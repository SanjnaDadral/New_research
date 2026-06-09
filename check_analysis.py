#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paper_analyzer.settings')
django.setup()

from analyzer.models import AnalysisResult

results = AnalysisResult.objects.all().order_by('-created_at')[:3]
for r in results:
    print(f"\n=== Analysis ID {r.id}: {r.document.title[:50]} ===")
    print(f"Summary: {r.summary[:100] if r.summary else 'EMPTY'}")
    print(f"Abstract: {r.abstract[:100] if r.abstract else 'EMPTY'}")
    print(f"Conclusion: {str(r.extras.get('conclusion', 'EMPTY')[:100]) if r.extras.get('conclusion') else 'EMPTY'}")
    print(f"References: {len(r.references) if r.references else 0} refs")
    print(f"Links: {len(r.extracted_links) if r.extracted_links else 0} links")
