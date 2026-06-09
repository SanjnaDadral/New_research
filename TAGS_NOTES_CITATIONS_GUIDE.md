# 📚 Complete Guide: Tags, Notes & Citations Features

## 📋 Table of Contents
1. [Add Tags - What & Why](#1-add-tags)
2. [Add Notes - What & Why](#2-add-notes)
3. [Citations - What & Why](#3-citations)
4. [Importance & Use Cases](#4-importance--use-cases)
5. [How to Use Each Feature](#5-how-to-use)

---

## 1️⃣ **ADD TAGS** 🏷️

### **What Are Tags?**

Tags are **short keywords or labels** you add to organize and categorize your analyzed papers. Think of them like hashtags or categories.

### **Example Tags:**
- `machine-learning`
- `covid-19`
- `important`
- `thesis-research`
- `needs-review`
- `deep-learning`
- `NLP`
- `for-paper`

### **What Tags Do:**

1. **Organization:**
   - Group similar papers together
   - Example: Tag all AI papers with `artificial-intelligence`

2. **Quick Filtering:**
   - Find all papers with specific tag
   - Example: See all papers tagged `important`

3. **Project Management:**
   - Track which papers are for which project
   - Example: `thesis-chapter-2`, `conference-2026`

4. **Status Tracking:**
   - Mark reading status
   - Example: `read`, `to-read`, `needs-citation`

5. **Topic Categorization:**
   - Organize by research topic
   - Example: `climate-change`, `economics`, `psychology`

### **How Tags Work:**

```
Paper 1: "AI in Healthcare"
Tags: [AI, healthcare, machine-learning, important]

Paper 2: "Deep Learning Methods"  
Tags: [AI, deep-learning, machine-learning]

Paper 3: "Climate Change Analysis"
Tags: [climate-change, data-science, important]

---
Search by tag "important":
→ Shows Paper 1 and Paper 3

Search by tag "AI":
→ Shows Paper 1 and Paper 2
```

### **Where Tags Are Stored:**

- Saved in **database** with your document
- Each document can have **unlimited tags**
- Tags are **unique per document** (no duplicates)
- Tags are **personal** (only you see your tags)

---

## 2️⃣ **ADD NOTES** 📝

### **What Are Notes?**

Notes are your **personal comments, thoughts, or observations** about a specific paper. Like writing in the margins of a physical book.

### **Example Notes:**

```
"This paper presents interesting methodology for 
sentiment analysis. Could be useful for my thesis 
Chapter 3. 

Key points:
- Uses BERT model
- 95% accuracy on Twitter dataset
- Code available on GitHub

TODO: Compare with Smith et al. (2024) approach
Need to cite this in literature review section"
```

### **What Notes Do:**

1. **Personal Annotations:**
   - Write your thoughts about the paper
   - Record ideas it sparks
   - Note connections to other research

2. **Key Points Extraction:**
   - Summarize main findings in your own words
   - Highlight important quotes
   - Mark crucial statistics

3. **Action Items:**
   - Track what you need to do with this paper
   - Example: "Need to read references", "Cite in intro"

4. **Research Planning:**
   - Note how paper fits in your research
   - Record which section to cite it in
   - Plan follow-up actions

5. **Critical Analysis:**
   - Write your critique
   - Note strengths and weaknesses
   - Record questions you have

### **How Notes Work:**

```
When viewing a paper result:
1. Click "Edit" button in Notes section
2. Text area appears
3. Type your notes (unlimited length)
4. Click "Save Notes"
5. Notes displayed when you return to paper
```

### **Notes Features:**

- **Rich Text:** Write paragraphs, lists, anything
- **Unlimited Length:** No character limit
- **Auto-Save:** Saved to database instantly
- **Private:** Only you can see your notes
- **Editable:** Update anytime
- **Searchable:** Can search notes in library (future feature)

---

## 3️⃣ **CITATIONS** 📖

### **What Are Citations?**

Citations are **properly formatted references** you can copy and paste into your research paper. Automatically generated in multiple academic styles.

### **Available Citation Styles:**

#### **1. APA (American Psychological Association)**
Most common in social sciences, education, psychology.

**Example:**
```
Smith, J., & Johnson, M. (2024). Deep Learning in Healthcare. 
Retrieved from https://example.com/paper
```

#### **2. MLA (Modern Language Association)**
Common in humanities, literature, arts.

**Example:**
```
Smith, John. "Deep Learning in Healthcare." 2024. 
Web. https://example.com/paper
```

#### **3. Chicago (Chicago Manual of Style)**
Common in history, arts, some sciences.

**Example:**
```
Smith, John, and Mary Johnson. "Deep Learning in Healthcare." 2024. 
https://example.com/paper
```

### **What Citations Do:**

1. **Automatic Formatting:**
   - Converts paper info to proper citation format
   - No need to manually format
   - Follows academic standards

2. **Multiple Styles:**
   - Switch between APA, MLA, Chicago
   - One click to copy any style
   - Use the one your professor/journal requires

3. **Copy to Clipboard:**
   - Click "Copy Citation" button
   - Paste directly into your paper
   - Saves time and prevents errors

4. **Include in Exports:**
   - PDF/Text exports include citation
   - Easy to keep track of sources

### **What Information Is Used:**

Citations are generated from:
- **Authors:** Extracted from paper (or "Unknown Author")
- **Publication Year:** Detected year (or "n.d." for no date)
- **Title:** Your document title
- **URL:** If uploaded from URL

### **How Citations Work:**

```
Your Paper Details:
- Authors: ["John Smith", "Mary Johnson"]
- Year: 2024
- Title: "AI in Healthcare"
- URL: https://example.com/paper

↓ Automatic Generation ↓

APA: Smith, J., & Johnson, M. (2024). AI in Healthcare. 
     Retrieved from https://example.com/paper

MLA: Smith, John. "AI in Healthcare." 2024. 
     Web. https://example.com/paper

Chicago: Smith, John, and Mary Johnson. "AI in Healthcare." 2024. 
         https://example.com/paper
```

---

## 4️⃣ **IMPORTANCE & USE CASES** 🎯

### **Why These Features Matter:**

#### **For Students:**

✅ **Tags:**
- Organize papers by class (`CS101`, `BIO202`)
- Track assignment papers (`midterm-project`, `final-paper`)
- Mark importance (`must-read`, `optional`)

✅ **Notes:**
- Write summaries for study
- Record professor's comments
- Note exam-relevant info

✅ **Citations:**
- Easy bibliography creation
- Correct formatting guaranteed
- Save hours of manual work

#### **For Researchers:**

✅ **Tags:**
- Organize by research project
- Track paper status (`reviewed`, `cited`, `pending`)
- Categorize methodology (`quantitative`, `qualitative`)

✅ **Notes:**
- Critical analysis documentation
- Methodology comparison notes
- Ideas for own research

✅ **Citations:**
- Build reference lists quickly
- Maintain consistency
- Export for LaTeX/Word

#### **For Literature Reviews:**

✅ **Tags:**
- `literature-review`, `background`, `methodology-papers`
- Track which papers cited where in your paper

✅ **Notes:**
- Key findings summary
- Relevance to your research
- Gaps identified

✅ **Citations:**
- Ready-to-use references
- Multiple papers = complete bibliography

---

## 5️⃣ **HOW TO USE EACH FEATURE** 🛠️

### **Using TAGS:**

#### **Step 1: View Paper Result**
```
Go to: /result/<document_id>/
Scroll to "Tags" section (purple icon)
```

#### **Step 2: Add Tag**
```
1. Find "Tags" section
2. Type tag name in input box
   Example: "machine-learning"
3. Click "Add" button
4. Tag appears immediately
```

#### **Step 3: Add Multiple Tags**
```
Repeat for each tag:
- "AI"
- "important"
- "thesis-chapter-3"
- "needs-review"
```

#### **Step 4: Remove Tag (If Needed)**
```
1. Click X on tag badge
2. Confirm removal
3. Tag deleted
```

#### **Best Practices:**
- **Use lowercase:** `machine-learning` not `Machine-Learning`
- **Use hyphens:** `machine-learning` not `machine learning`
- **Be consistent:** Always use same tag format
- **Keep short:** `ML` or `machine-learning` (not `machine-learning-and-AI`)
- **Create system:** Decide tag categories beforehand

#### **Tag Examples by Category:**

**Topics:**
- `artificial-intelligence`
- `machine-learning`
- `deep-learning`
- `NLP`
- `computer-vision`

**Status:**
- `read`
- `to-read`
- `cited`
- `needs-citation`
- `reviewed`

**Projects:**
- `thesis-2026`
- `conference-paper`
- `research-project-1`
- `grant-proposal`

**Importance:**
- `important`
- `critical`
- `reference-only`
- `background`

**Methodology:**
- `quantitative`
- `qualitative`
- `survey`
- `experimental`

---

### **Using NOTES:**

#### **Step 1: View Paper Result**
```
Go to: /result/<document_id>/
Scroll to "My Notes" section (yellow/orange icon)
```

#### **Step 2: Click Edit**
```
1. Click "Edit" button
2. Text area appears
3. See existing notes (if any)
```

#### **Step 3: Write Notes**
```
Type anything you want:
- Summaries
- Key points
- Personal thoughts
- Action items
- Questions
- Critique
```

#### **Step 4: Save**
```
1. Click "Save Notes" button
2. Notes saved to database
3. View mode returns
4. Can edit again anytime
```

#### **Note-Taking Template (Suggested):**

```
=== KEY FINDINGS ===
- Main finding 1
- Main finding 2
- Main finding 3

=== METHODOLOGY ===
- Approach used
- Dataset details
- Tools/models

=== RELEVANCE TO MY RESEARCH ===
- How this connects to my work
- Which section to cite in

=== STRENGTHS ===
+ What this paper does well

=== LIMITATIONS ===
- Weaknesses or gaps
- What could be improved

=== ACTION ITEMS ===
[ ] Cite in literature review
[ ] Compare with Smith (2024)
[ ] Download code from GitHub

=== QUESTIONS ===
? How does this compare to...?
? Could I replicate this?
```

---

### **Using CITATIONS:**

#### **Step 1: View Paper Result**
```
Go to: /result/<document_id>/
Scroll to "Citation" section (blue icon)
```

#### **Step 2: Choose Style**
```
See 3 buttons:
- [APA] ← Default
- [MLA]
- [Chicago]

Click the one you need
```

#### **Step 3: View Citation**
```
Citation appears in box below buttons
Formatted correctly for that style
```

#### **Step 4: Copy Citation**
```
1. Click "Copy Citation" button
2. See "Copied!" confirmation
3. Paste in your document
```

#### **Using in Your Paper:**

**In Microsoft Word:**
```
1. Go to References section of your paper
2. Paste copied citation
3. Done!
```

**In Google Docs:**
```
1. Go to Bibliography
2. Paste citation
3. Format if needed
```

**In LaTeX:**
```
1. Convert to BibTeX format (or manually format)
2. Add to .bib file
```

#### **Multiple Papers:**
```
For each paper:
1. Open result page
2. Copy citation
3. Paste in reference list
4. Repeat for all papers

Result: Complete bibliography!
```

---

## 📊 **Comparison Table**

| Feature | Purpose | When to Use | Benefit |
|---------|---------|-------------|---------|
| **Tags** | Organization & Filtering | Organizing many papers | Quick categorization |
| **Notes** | Personal comments | Recording thoughts | Detailed annotations |
| **Citations** | Reference formatting | Writing papers | Proper citations |

---

## 🎯 **Real-World Workflow Example**

### **Scenario: PhD Student Writing Thesis**

#### **Paper 1: "Deep Learning in Healthcare"**

**1. Analyze paper** → Upload PDF  
**2. Add tags:**
```
- healthcare
- deep-learning
- thesis-chapter-2
- important
- cite-in-intro
```

**3. Add notes:**
```
Excellent methodology section - similar to what I'm doing.
Uses CNN architecture on medical images.
97% accuracy - need to compare with my results.

TODO: 
- Cite in Chapter 2, Section 2.3
- Compare their dataset with mine
- Check their GitHub for code

Key quote: "Deep learning models outperform traditional 
methods by 15%" (page 7)
```

**4. Copy citation (APA):**
```
Smith, J., & Lee, M. (2024). Deep Learning in Healthcare. 
Journal of Medical AI, 15(3), 234-251.
```

**5. Paste in thesis bibliography** → Done!

---

#### **Later: Finding Papers for Chapter 2**

**In Library view:**
```
Filter by tag: "thesis-chapter-2"
→ Shows all relevant papers
→ Read notes to remember why each is important
→ Copy citations to build reference list
```

---

## ✅ **Best Practices Summary**

### **Tags:**
✅ Keep consistent format  
✅ Use 3-5 tags per paper  
✅ Create tag system beforehand  
✅ Review and clean up periodically  

### **Notes:**
✅ Write notes immediately after reading  
✅ Use structured template  
✅ Include page numbers for quotes  
✅ Record action items  
✅ Update notes as needed  

### **Citations:**
✅ Copy citation right away  
✅ Double-check author names  
✅ Verify year is correct  
✅ Use style guide requires  
✅ Keep organized bibliography  

---

## 🎓 **Academic Writing Tips**

### **Using These Features for A+ Papers:**

1. **Literature Review Process:**
   ```
   Analyze 20 papers →
   Tag by topic →
   Write notes on each →
   Copy all citations →
   Create reference list →
   Write review using notes →
   Done in half the time!
   ```

2. **Citation Management:**
   ```
   Instead of: Manually typing each citation (error-prone)
   Use: Copy from PaperAIzer (accurate, fast)
   ```

3. **Paper Organization:**
   ```
   Instead of: Folders and folders of PDFs
   Use: Tags to categorize everything
   ```

---

## 💡 **Pro Tips**

### **Tags:**
- Create a "master tag list" document
- Use prefixes: `topic:AI`, `status:read`, `project:thesis`
- Don't over-tag (3-5 tags is ideal)

### **Notes:**
- Use Markdown format for structure
- Include date when writing notes
- Link to other papers in notes
- Export notes periodically as backup

### **Citations:**
- Always copy citation immediately
- Keep a "papers to cite" list with tags
- Verify citation details match paper
- Use citation manager integration (future feature)

---

## 🔮 **Future Enhancements (Suggestions)**

### **Tags:**
- [ ] Auto-suggest tags based on keywords
- [ ] Tag cloud visualization
- [ ] Export papers by tag
- [ ] Shared tags for teams

### **Notes:**
- [ ] Markdown rendering
- [ ] Note search across all papers
- [ ] Export all notes
- [ ] Voice note recording

### **Citations:**
- [ ] More citation styles (IEEE, Harvard, Vancouver)
- [ ] BibTeX export
- [ ] Citation manager integration (Zotero, Mendeley)
- [ ] Bulk citation export

---

## ❓ **FAQ**

### **Q: Can others see my tags and notes?**
**A:** No, they are private. Only you can see them.

### **Q: How many tags can I add?**
**A:** Unlimited! But 3-5 tags per paper is recommended.

### **Q: Can I search by tags?**
**A:** Yes, in the library view you can filter by tags.

### **Q: Are citations accurate?**
**A:** Citations use extracted data. Always verify details match the original paper.

### **Q: Can I edit notes after saving?**
**A:** Yes! Click "Edit" anytime to update.

### **Q: Do tags and notes export with PDF?**
**A:** Notes appear in exports. Tags export feature coming soon.

### **Q: Can I bulk-edit tags?**
**A:** Currently one paper at a time. Bulk edit coming soon.

---

## ✅ **Summary**

| Feature | What It Does | Why Important |
|---------|--------------|---------------|
| **Tags** | Label and categorize papers | Quick organization & filtering |
| **Notes** | Write personal observations | Remember key insights |
| **Citations** | Generate formatted references | Save time on bibliography |

**All three features work together** to help you:
- ✅ Organize research papers efficiently
- ✅ Remember important insights
- ✅ Build bibliographies quickly
- ✅ Manage academic projects professionally

---

**Start using these features today to supercharge your research workflow!** 🚀
