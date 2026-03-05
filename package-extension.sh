#!/bin/bash

# Package Sidebar Scholar extension for Chrome Web Store submission
# This script creates a ZIP file with all necessary extension files

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="$SCRIPT_DIR/frontend"
OUTPUT_FILE="$SCRIPT_DIR/sidebar-scholar-extension.zip"

echo "📦 Packaging Sidebar Scholar extension..."

# Change to frontend directory
cd "$FRONTEND_DIR"

# Remove old ZIP if it exists
if [ -f "$OUTPUT_FILE" ]; then
    echo "Removing old package..."
    rm "$OUTPUT_FILE"
fi

# Create ZIP file, excluding unnecessary files
echo "Creating ZIP package..."
zip -r "$OUTPUT_FILE" . \
    -x "*.DS_Store" \
    -x "*.git*" \
    -x "store-assets/*" \
    -x "*.md" \
    -x "LOAD_EXTENSION.md" \
    -x "icons/README.md"

# Verify ZIP contents
echo ""
echo "✅ Package created: $OUTPUT_FILE"
echo ""
echo "📋 Package contents:"
unzip -l "$OUTPUT_FILE" | head -20

echo ""
echo "✨ Ready for Chrome Web Store submission!"
echo "   Upload: $OUTPUT_FILE"
