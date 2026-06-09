import json
import logging
import base64
import re
from django.conf import settings
from groq import Groq

logger = logging.getLogger(__name__)

def rag_pipeline(text: str, query: str = "Summarize this research paper"):
    try:
        text = text or ""
        if len(text.strip()) < 20:
            return {"summary": "Not enough content in the document to analyze."}

        if not settings.GROQ_API_KEY or not settings.GROQ_API_KEY.strip():
            from analyzer.ml_model import MLProcessor
            ml = MLProcessor()
            result = ml.full_analysis(text)
            return {"summary": result.get("summary") or result.get("native_summary", "Analysis unavailable.")}

        client = Groq(api_key=settings.GROQ_API_KEY)

        MAX_CHARS = 30000
        context = text[:MAX_CHARS]
        user_question = (query or "Summarize this research paper").strip()

        prompt = f"""You are an expert research assistant. Answer the user's question using ONLY the document context below.
If the answer is not in the context, say so clearly.

QUESTION:
{user_question}

DOCUMENT CONTEXT:
{context}
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an expert academic research assistant. Answer concisely and accurately."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500,
        )

        return {
            "summary": response.choices[0].message.content
        }

    except Exception as e:
        logger.error("GROQ Pipeline Error", exc_info=True)
        return {
            "summary": f"Error analyzing the paper: {str(e)}"
        }

def _sanitize_json_content(content: str) -> str:
    """Strip markdown fences and invalid control chars from Groq output."""
    content = (content or "").strip()
    if content.startswith('```'):
        content = content.split('```')[1]
        if content.startswith('json'):
            content = content[4:]
        content = content.strip()
    if content.endswith('```'):
        content = content[:-3].strip()
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', content)


def _extract_text_field(content: str, field: str) -> str:
    """Best-effort extraction when Groq returns malformed JSON."""
    match = re.search(
        rf'"{field}"\s*:\s*"((?:[^"\\]|\\.)*)"',
        content,
        re.DOTALL,
    )
    if match:
        return match.group(1).replace('\\n', '\n').replace('\\"', '"').strip()
    match = re.search(
        rf'"{field}"\s*:\s*([\s\S]*?)(?=\n\s*"[a-zA-Z_]+"\s*:|$)',
        content,
    )
    if match:
        value = match.group(1).strip().rstrip(',').strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        return value.strip()
    return ""


def _extract_list_field(content: str, field: str) -> list:
    """Extract a JSON array field from malformed Groq output."""
    match = re.search(rf'"{field}"\s*:\s*(\[[\s\S]*?\])', content)
    if not match:
        return []
    try:
        parsed = json.loads(match.group(1))
        return parsed if isinstance(parsed, list) else []
    except json.JSONDecodeError:
        return []


def _parse_groq_json(content: str) -> dict:
    """Parse Groq JSON with repair and field extraction fallbacks."""
    content = _sanitize_json_content(content)
    if not content:
        return {}

    try:
        parsed = json.loads(content)
        return parsed if isinstance(parsed, dict) else {}
    except json.JSONDecodeError as e:
        logger.warning(f"JSON parse error: {e}, attempting field extraction")

    repaired = {
        "summary": _extract_text_field(content, "summary"),
        "abstract": _extract_text_field(content, "abstract"),
        "goal": _extract_text_field(content, "goal"),
        "impact": _extract_text_field(content, "impact"),
        "conclusion": _extract_text_field(content, "conclusion"),
        "publication_year": _extract_text_field(content, "publication_year"),
        "keywords": _extract_list_field(content, "keywords"),
        "methodology": _extract_list_field(content, "methodology"),
        "technologies": _extract_list_field(content, "technologies"),
        "research_gaps": _extract_list_field(content, "research_gaps"),
        "datasets": _extract_list_field(content, "datasets"),
        "authors": _extract_list_field(content, "authors"),
    }
    if not repaired["summary"] and not repaired["abstract"]:
        repaired["summary"] = content[:1500]
    return repaired


def _has_meaningful_analysis(data: dict) -> bool:
    """Return True when Groq produced usable structured output."""
    if not data:
        return False
    list_fields = ("keywords", "methodology", "technologies", "authors")
    if any(isinstance(data.get(field), list) and data.get(field) for field in list_fields):
        return True
    text_fields = ("summary", "abstract", "goal", "impact", "conclusion")
    for field in text_fields:
        value = str(data.get(field, "")).strip()
        if len(value) > 80 and not value.startswith("{"):
            return True
    return False


def _pick_richer_text(primary: str, fallback: str, min_useful: int = 80) -> str:
    """Prefer the longer, more informative text version."""
    primary = str(primary or "").strip()
    fallback = str(fallback or "").strip()
    if primary.startswith("{") or '"summary"' in primary[:80]:
        primary = ""
    if len(primary) < min_useful and fallback:
        return fallback
    if len(fallback) > len(primary) * 1.35 and len(fallback) >= min_useful:
        return fallback
    return primary or fallback


def _merge_with_ml(groq_data: dict, ml_data: dict) -> dict:
    """Fill missing Groq fields from the local ML processor."""
    merged = dict(groq_data or {})
    list_fields = (
        "keywords", "methodology", "technologies", "authors",
        "research_gaps", "datasets", "references", "extracted_links",
    )
    text_fields = (
        "summary", "abstract", "goal", "impact", "conclusion",
        "publication_year", "methodology_summary", "title",
    )

    for field in list_fields:
        current = merged.get(field)
        fallback = ml_data.get(field, [])
        if not current:
            merged[field] = fallback
        elif isinstance(current, list) and isinstance(fallback, list) and len(fallback) > len(current):
            merged[field] = list(dict.fromkeys(current + fallback))

    for field in text_fields:
        merged[field] = _pick_richer_text(merged.get(field, ""), ml_data.get(field, ""))

    merged["summary"] = _pick_richer_text(
        merged.get("summary", ""),
        ml_data.get("native_summary") or ml_data.get("summary", ""),
        min_useful=120,
    )
    merged["abstract"] = _pick_richer_text(merged.get("abstract", ""), ml_data.get("abstract", ""), min_useful=100)
    merged["impact"] = _pick_richer_text(merged.get("impact", ""), ml_data.get("impact", ""), min_useful=100)
    merged["conclusion"] = _pick_richer_text(
        merged.get("conclusion", ""),
        ml_data.get("conclusion", ""),
        min_useful=100,
    )

    if not merged.get("native_summary"):
        merged["native_summary"] = ml_data.get("native_summary", "")

    return merged


def analyze_text_with_groq(text: str, prompt: str = "Summarize this:") -> dict:
    """
    Analyze research paper using Groq AI with automatic fallback to ml_processor.
    Returns a dict with structured analysis keys — never a plain str.
    """
    from analyzer.ml_model import MLProcessor

    word_count = len(text.split())
    unique_words = len(set(text.split()))

    def _safe_dict(summary: str) -> dict:
        return {
            "summary": summary,
            "abstract": "",
            "keywords": [],
            "methodology": [],
            "technologies": [],
            "goal": "",
            "impact": "",
            "publication_year": "",
            "authors": [],
            "research_gaps": [],
            "conclusion": "",
            "statistics": {"word_count": word_count, "unique_words": unique_words},
        }

    try:
        ml = MLProcessor()
        ml_data = ml.full_analysis(text)
    except Exception as ml_error:
        logger.error(f"ML processor unavailable: {ml_error}")
        ml_data = {}

    if not settings.GROQ_API_KEY or not settings.GROQ_API_KEY.strip():
        logger.warning("GROQ_API_KEY not set in .env - using ML processor fallback")
        if ml_data:
            ml_data["statistics"] = {"word_count": word_count, "unique_words": unique_words}
            return ml_data
        return _safe_dict(
            "Analysis failed: No AI service available (set GROQ_API_KEY in .env or ensure ML models are working)"
        )

    TEXT_CAP_70B = 18000
    TEXT_CAP_8B = 12000

    analysis_prompt_template = """Analyze the following research paper in depth and return a JSON object with EXACTLY these keys:
{{
  "summary": "detailed executive summary, 300-450 words covering problem, approach, methods, results, and significance",
  "abstract": "full paper abstract or reconstructed abstract, 200-350 words",
  "keywords": ["keyword1", "keyword2", "..."],
  "methodology": ["method1", "method2", "..."],
  "technologies": ["tech1", "tech2", "..."],
  "goal": "primary research objective and motivation, 3-5 sentences",
  "impact": "contributions, results, and real-world applications, 200-300 words",
  "research_gaps": ["gap1", "gap2", "gap3"],
  "conclusion": "detailed conclusion with key findings and future work, 150-250 words",
  "datasets": ["dataset1"],
  "authors": ["author1"],
  "publication_year": "2024"
}}

Rules:
- Return ONLY valid JSON
- Be thorough and specific — include numbers, metrics, and named methods when present
- Every string value MUST be quoted
- Arrays must use JSON array syntax
- Do not include markdown fences

TEXT:
{text}"""

    def _call_groq(model: str, text_cap: int):
        client = Groq(api_key=settings.GROQ_API_KEY)
        trimmed = text[:text_cap]
        full_prompt = analysis_prompt_template.format(text=trimmed)
        return client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a research paper analyzer. "
                        "Respond with one valid JSON object only. "
                        "All string values must be properly quoted."
                    ),
                },
                {"role": "user", "content": full_prompt},
            ],
            temperature=0.2,
            max_tokens=4096,
            response_format={"type": "json_object"},
        )

    data = {}
    try:
        response = _call_groq("llama-3.3-70b-versatile", TEXT_CAP_70B)
        data = _parse_groq_json(response.choices[0].message.content)
    except Exception as e:
        logger.warning(f"Groq 70b model failed ({str(e)[:100]}), trying 8b fallback...")
        try:
            response = _call_groq("llama-3.1-8b-instant", TEXT_CAP_8B)
            data = _parse_groq_json(response.choices[0].message.content)
        except Exception as e2:
            logger.error(f"Groq models exhausted, using ML processor: {e2}")
            data = {}

    if not _has_meaningful_analysis(data):
        logger.warning("Groq output incomplete - enriching with ML processor results")
        if ml_data:
            data = _merge_with_ml(data, ml_data)
        elif not data:
            return _safe_dict("Analysis could not be completed. Please try again.")
    elif ml_data:
        data = _merge_with_ml(data, ml_data)

    data["statistics"] = {"word_count": word_count, "unique_words": unique_words}
    data.setdefault("research_gaps", [])
    data.setdefault("conclusion", "")
    data.setdefault("datasets", [])
    data.setdefault("keywords", [])
    data.setdefault("methodology", [])
    data.setdefault("technologies", [])
    data.setdefault("authors", [])

    logger.info(
        "Analysis completed - summary: %s chars, keywords: %s, methodology: %s",
        len(str(data.get("summary", ""))),
        len(data.get("keywords", [])),
        len(data.get("methodology", [])),
    )
    return data

def analyze_image_with_groq(image_file) -> dict:
    """
    Analyze a research paper image using Groq Vision model.
    """
    try:
        client = Groq(api_key=settings.GROQ_API_KEY)
        
        # Read and encode image
        image_file.seek(0)
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        prompt = """
        Analyze this research paper image and provide a comprehensive JSON extraction.
        Extract all text first, then provide:
        - summary: A clear executive summary of what this image shows.
        - content_text: The full text extracted from the image.
        - keywords: List of technical keywords.
        - goal: The primary objective mentioned.
        - authors: Any author names found.
        - publication_year: Year of publication if found.
        
        Return ONLY valid JSON.
        """
        
        response = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            temperature=0.3,
            max_tokens=2048,
        )
        
        content = response.choices[0].message.content.strip()
        
        # Clean up JSON
        if content.startswith('```'):
            content = content.split('```')[1]
            if content.startswith('json'):
                content = content[4:]
            content = content.strip()
        if content.endswith('```'):
            content = content[:-3].strip()
            
        try:
            data = json.loads(content)
        except:
            data = {"summary": content, "content_text": content}
            
        # Standardize for AnalysisResult
        final_data = {
            "summary": data.get("summary", ""),
            "abstract": data.get("content_text", ""),
            "keywords": data.get("keywords", []),
            "methodology": [],
            "technologies": [],
            "goal": data.get("goal", ""),
            "impact": "",
            "publication_year": data.get("publication_year", ""),
            "authors": data.get("authors", []),
            "statistics": {"word_count": len(data.get("content_text", "").split()), "unique_words": 0},
            "research_gaps": [],
            "conclusion": "",
            "content_text": data.get("content_text", "")
        }
        
        return final_data
        
    except Exception as e:
        logger.error(f"Groq Vision error: {e}", exc_info=True)
        return {
            "summary": f"Error analyzing image: {str(e)}",
            "content_text": "",
            "statistics": {"word_count": 0, "unique_words": 0}
        }