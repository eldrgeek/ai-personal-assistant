#!/bin/bash

echo "🚀 Launching Chrome with debugging enabled..."

# Create debug profile directory
mkdir -p chrome-debug-profile

# Launch Chrome with debugging
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --remote-allow-origins="*" \
  --no-first-run \
  --no-default-browser-check \
  --disable-features=VizDisplayCompositor \
  --user-data-dir="./chrome-debug-profile" \
  --new-window \
  --background

echo "✅ Chrome launched with debugging on port 9222"
echo "🌐 Debug URL: http://localhost:9222"
echo "📁 Profile directory: ./chrome-debug-profile"
echo ""
echo "Chrome should now be running. You can:"
echo "1. Choose your profile in the new Chrome window"
echo "2. Navigate to https://dashboard.render.com"
echo "3. Use the MCP tools to automate the setup"
