#!/bin/bash

echo "🚀 AI Personal Assistant - Deployment Setup"
echo "============================================="
echo ""

# Check if required tools are installed
echo "🔍 Checking required tools..."
if ! command -v netlify &> /dev/null; then
    echo "❌ Netlify CLI not found. Please install it first:"
    echo "   npm install -g netlify-cli"
    echo "   netlify login"
    exit 1
fi

if ! command -v render &> /dev/null; then
    echo "❌ Render CLI not found. Please install it first:"
    echo "   npm install -g @render/cli"
    echo "   render login"
    exit 1
fi

echo "✅ All required tools are installed"
echo ""

# Check login status
echo "🔐 Checking login status..."
if ! netlify status &> /dev/null; then
    echo "❌ Not logged into Netlify. Please run: netlify login"
    exit 1
fi

if ! render whoami &> /dev/null; then
    echo "❌ Not logged into Render. Please run: render login"
    exit 1
fi

echo "✅ Logged into both services"
echo ""

# Show next steps
echo "📋 Next Steps for Deployment:"
echo "=============================="
echo ""
echo "1. 🌐 Deploy Frontend to Netlify:"
echo "   cd frontend"
echo "   netlify sites:create --name ai-personal-assistant"
echo "   npm run build"
echo "   netlify deploy --prod --dir=dist"
echo ""
echo "2. ☁️  Deploy Backend to Render:"
echo "   cd .."
echo "   render deploy"
echo ""
echo "3. 🔑 Get Required Information:"
echo "   - Netlify Site ID (from netlify status)"
echo "   - Netlify Auth Token (from netlify user:list)"
echo "   - Render Webhook URL (from render dashboard)"
echo ""
echo "4. ⚙️  Configure GitHub Secrets:"
echo "   Go to: https://github.com/eldrgeek/ai-personal-assistant/settings/secrets/actions"
echo "   Add: NETLIFY_AUTH_TOKEN, NETLIFY_SITE_ID, RENDER_WEBHOOK_URL"
echo ""
echo "5. 🚀 Test Automatic Deployment:"
echo "   git push origin main"
echo "   Watch GitHub Actions deploy automatically!"
echo ""
echo "📚 For detailed instructions, see DEPLOYMENT.md"
echo ""
echo "🎯 Ready to deploy? Run: ./deploy.sh"
