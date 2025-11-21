#!/bin/bash
# Setup fonts for GitHub Actions (Linux environment)
# This script copies bundled fonts to system font directory

echo "📦 Setting up Arabic fonts for Cairo/Pango..."

# Create user fonts directory if it doesn't exist
mkdir -p ~/.fonts

# Copy Arabic fonts
echo "📝 Copying Arabic fonts..."
cp -r fonts/arabic/amiri/Amiri-1.000/*.ttf ~/.fonts/ 2>/dev/null || true
cp -r fonts/arabic/scheherazade/ScheherazadeNew-4.000/*.ttf ~/.fonts/ 2>/dev/null || true
cp -r fonts/arabic/noto/NotoNaskhArabic/full/ttf/*.ttf ~/.fonts/ 2>/dev/null || true

# Copy Quran font
echo "📖 Copying Quran font..."
cp fonts/quran/hafs.ttf ~/.fonts/ 2>/dev/null || true

# Copy Product Sans (English)
echo "🔤 Copying English fonts..."
cp fonts/ProductSans*.ttf ~/.fonts/ 2>/dev/null || true

# Update font cache
echo "🔄 Updating font cache..."
fc-cache -f -v ~/.fonts

# Verify fonts are available
echo ""
echo "✅ Installed fonts:"
fc-list | grep -E "(Amiri|Scheherazade|Noto Naskh|Product Sans|hafs)" || echo "⚠️  No fonts found in cache yet"

echo ""
echo "✅ Font setup complete!"
