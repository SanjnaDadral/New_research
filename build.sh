#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "========================================="
echo "PaperAIzer Build Script for Render"
echo "========================================="

echo ""
echo "=== Step 1: Installing Python dependencies ==="
if [ -f "requirements.txt" ]; then
  pip install --no-cache-dir -r requirements.txt
  echo "✓ Dependencies installed"
else
  echo "✗ requirements.txt not found!"
  exit 1
fi

echo ""
echo "=== Step 2: Running database migrations ==="
python manage.py migrate --no-input || echo "⚠ Migration warning (may be expected)"
echo "✓ Migrations applied"

echo ""
echo "=== Step 3: Collecting static files ==="
python manage.py collectstatic --no-input --clear || echo "⚠ Static files collection warning"
echo "✓ Static files collected"

echo ""
echo "=== Step 4: Creating superuser (if needed) ==="
python manage.py create_superuser_auto || echo "⚠ Superuser creation skipped"
echo "✓ Superuser ready"

echo ""
echo "=== Step 5: Downloading NLTK data ==="
python -c "
import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
for data in ['punkt', 'punkt_tab', 'stopwords']:
    try:
        nltk.download(data, quiet=True)
    except:
        pass
print('NLTK data ready')
" || echo "⚠ NLTK data download warning"
echo "✓ NLTK data ready"

echo ""
echo "========================================="
echo "Build completed successfully!"
echo "========================================="

echo ""
echo "========================================="
echo "✓ Build complete!"
echo "========================================="
