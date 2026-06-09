"""
Management command to verify bulk upload feature is properly configured
"""
from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Check if bulk upload feature is properly configured and accessible'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Bulk Upload Feature Diagnostic'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        
        issues = []
        
        # 1. Check template exists
        self.stdout.write(self.style.SUCCESS('\n1. TEMPLATE FILES:'))
        
        upload_template = settings.BASE_DIR / 'templates' / 'analyzer' / 'upload.html'
        if upload_template.exists():
            self.stdout.write('   ✅ upload.html exists')
            
            # Check for bulk upload code
            content = upload_template.read_text()
            if 'panel-bulk' in content:
                self.stdout.write('   ✅ Bulk upload panel found in template')
            else:
                self.stdout.write(self.style.ERROR('   ❌ Bulk upload panel NOT found in template'))
                issues.append('Bulk upload panel missing from upload.html')
            
            if 'data-tab="bulk"' in content:
                self.stdout.write('   ✅ Bulk upload tab found in template')
            else:
                self.stdout.write(self.style.ERROR('   ❌ Bulk upload tab NOT found in template'))
                issues.append('Bulk upload tab missing from upload.html')
                
            if 'bulkFiles' in content:
                self.stdout.write('   ✅ Bulk files input found in template')
            else:
                self.stdout.write(self.style.ERROR('   ❌ Bulk files input NOT found'))
                issues.append('Bulk files input missing from template')
        else:
            self.stdout.write(self.style.ERROR('   ❌ upload.html does NOT exist'))
            issues.append('Upload template missing')
        
        # 2. Check static files
        self.stdout.write(self.style.SUCCESS('\n2. STATIC FILES:'))
        
        static_root = getattr(settings, 'STATIC_ROOT', None)
        if static_root:
            self.stdout.write(f'   Static root: {static_root}')
            
            # Check if collected
            if os.path.exists(static_root):
                self.stdout.write('   ✅ Static root exists')
                
                # Check for JS files
                js_path = os.path.join(static_root, 'js')
                if os.path.exists(js_path):
                    js_files = os.listdir(js_path)
                    self.stdout.write(f'   ✅ JS files found: {len(js_files)} files')
                    if 'app.js' in js_files:
                        self.stdout.write('   ✅ app.js present')
                    if 'analysis_handler.js' in js_files:
                        self.stdout.write('   ✅ analysis_handler.js present')
                else:
                    self.stdout.write(self.style.WARNING('   ⚠️  JS directory not found'))
                    issues.append('Run: python manage.py collectstatic')
                
                # Check for CSS files
                css_path = os.path.join(static_root, 'css')
                if os.path.exists(css_path):
                    css_files = os.listdir(css_path)
                    self.stdout.write(f'   ✅ CSS files found: {len(css_files)} files')
                else:
                    self.stdout.write(self.style.WARNING('   ⚠️  CSS directory not found'))
            else:
                self.stdout.write(self.style.WARNING('   ⚠️  Static files not collected'))
                issues.append('Run: python manage.py collectstatic')
        else:
            self.stdout.write(self.style.WARNING('   ⚠️  STATIC_ROOT not configured'))
        
        # 3. Check view implementation
        self.stdout.write(self.style.SUCCESS('\n3. BACKEND VIEW:'))
        
        views_file = settings.BASE_DIR / 'analyzer' / 'views.py'
        if views_file.exists():
            self.stdout.write('   ✅ views.py exists')
            
            content = views_file.read_text()
            if "input_type == 'bulk'" in content:
                self.stdout.write('   ✅ Bulk upload handler found in views')
            else:
                self.stdout.write(self.style.ERROR('   ❌ Bulk upload handler NOT found in views'))
                issues.append('Bulk upload handler missing from views.py')
            
            if 'bulk_files = request.FILES.getlist' in content:
                self.stdout.write('   ✅ Bulk files processing implemented')
            else:
                self.stdout.write(self.style.ERROR('   ❌ Bulk files processing NOT implemented'))
                issues.append('Bulk files processing missing from views.py')
        else:
            self.stdout.write(self.style.ERROR('   ❌ views.py does NOT exist'))
            issues.append('Views file missing')
        
        # 4. Check URL configuration
        self.stdout.write(self.style.SUCCESS('\n4. URL CONFIGURATION:'))
        
        urls_file = settings.BASE_DIR / 'analyzer' / 'urls.py'
        if urls_file.exists():
            self.stdout.write('   ✅ urls.py exists')
            
            content = urls_file.read_text()
            if 'analyze_document' in content:
                self.stdout.write('   ✅ analyze_document URL configured')
            else:
                self.stdout.write(self.style.ERROR('   ❌ analyze_document URL NOT configured'))
                issues.append('analyze_document URL missing')
            
            if 'bulk-results' in content or 'bulk_results' in content:
                self.stdout.write('   ✅ bulk_results URL configured')
            else:
                self.stdout.write(self.style.WARNING('   ⚠️  bulk_results URL not found'))
        else:
            self.stdout.write(self.style.ERROR('   ❌ urls.py does NOT exist'))
        
        # 5. Check settings
        self.stdout.write(self.style.SUCCESS('\n5. SETTINGS:'))
        
        max_upload = getattr(settings, 'FILE_UPLOAD_MAX_MEMORY_SIZE', 0)
        max_data = getattr(settings, 'DATA_UPLOAD_MAX_MEMORY_SIZE', 0)
        
        self.stdout.write(f'   Max file upload: {max_upload / (1024*1024):.0f} MB')
        self.stdout.write(f'   Max data upload: {max_data / (1024*1024):.0f} MB')
        
        if max_upload >= 50 * 1024 * 1024:
            self.stdout.write('   ✅ File upload limit sufficient (≥50 MB)')
        else:
            self.stdout.write(self.style.WARNING(f'   ⚠️  File upload limit may be too low'))
            issues.append('Increase FILE_UPLOAD_MAX_MEMORY_SIZE to at least 50MB')
        
        # 6. Feature accessibility summary
        self.stdout.write(self.style.SUCCESS('\n6. ACCESSIBILITY:'))
        
        self.stdout.write('\n   To access bulk upload:')
        self.stdout.write('   1. Go to /upload/')
        self.stdout.write('   2. Look for 3 tabs: PDF Upload | URL/Link | Bulk Upload')
        self.stdout.write('   3. Click "Bulk Upload" tab (third one)')
        self.stdout.write('   4. Drag & drop or select 2-5 files')
        self.stdout.write('   5. Click "Analyze Paper"')
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
        self.stdout.write(self.style.SUCCESS('SUMMARY:'))
        
        if not issues:
            self.stdout.write(self.style.SUCCESS('\n   ✅ ALL CHECKS PASSED!'))
            self.stdout.write(self.style.SUCCESS('   Bulk upload feature is properly configured.\n'))
            self.stdout.write('   If users cannot see it:')
            self.stdout.write('   - Tell them to hard refresh (Ctrl+Shift+R)')
            self.stdout.write('   - Clear browser cache')
            self.stdout.write('   - Try different browser')
            self.stdout.write('   - Check on desktop (not mobile)')
        else:
            self.stdout.write(self.style.ERROR(f'\n   ❌ {len(issues)} issue(s) found:\n'))
            for i, issue in enumerate(issues, 1):
                self.stdout.write(f'   {i}. {issue}')
            
            self.stdout.write(self.style.WARNING('\n   💡 FIXES:'))
            if 'collectstatic' in ' '.join(issues):
                self.stdout.write('   Run: python manage.py collectstatic --no-input')
            if any('template' in issue.lower() for issue in issues):
                self.stdout.write('   Check templates/analyzer/upload.html file')
            if any('views' in issue.lower() for issue in issues):
                self.stdout.write('   Check analyzer/views.py file')
        
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 60 + '\n'))
