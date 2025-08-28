#!/bin/bash

echo "🚀 AI Personal Assistant - Deployment Script"
echo "=============================================="

# Check if required tools are installed
check_tool() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 is not installed. Please install it first."
        exit 1
    else
        echo "✅ $1 is installed"
    fi
}

echo "🔍 Checking required tools..."
check_tool "netlify"
check_tool "render"

# Function to deploy to Netlify
deploy_netlify() {
    echo ""
    echo "🌐 Deploying to Netlify..."
    
    # Build the frontend
    echo "📦 Building frontend..."
    cd frontend
    npm run build
    
    # Deploy to Netlify
    echo "🚀 Deploying to Netlify..."
    netlify deploy --prod --dir=dist
    
    cd ..
    echo "✅ Netlify deployment completed!"
}

# Function to deploy to Render
deploy_render() {
    echo ""
    echo "☁️  Deploying to Render..."
    
    # Check if render.yaml exists
    if [ ! -f "render.yaml" ]; then
        echo "❌ render.yaml not found. Please create it first."
        return 1
    fi
    
    # Deploy to Render
    echo "🚀 Deploying to Render..."
    render deploy
    
    echo "✅ Render deployment completed!"
}

# Function to setup GitHub secrets
setup_github_secrets() {
    echo ""
    echo "🔑 Setting up GitHub Secrets..."
    echo ""
    echo "You need to add these secrets to your GitHub repository:"
    echo "Go to: https://github.com/eldrgeek/ai-personal-assistant/settings/secrets/actions"
    echo ""
    echo "Required secrets:"
    echo "1. NETLIFY_AUTH_TOKEN - Get from: https://app.netlify.com/user/applications#personal-access-tokens"
    echo "2. NETLIFY_SITE_ID - Get from your Netlify site settings"
    echo "3. RENDER_WEBHOOK_URL - Get from your Render service webhooks"
    echo ""
    echo "After adding these secrets, push to main branch to trigger automatic deployment!"
}

# Main menu
show_menu() {
    echo ""
    echo "What would you like to do?"
    echo "1. Deploy to Netlify (Frontend)"
    echo "2. Deploy to Render (Backend)"
    echo "3. Deploy to both"
    echo "4. Setup GitHub secrets for automatic deployment"
    echo "5. Exit"
    echo ""
    read -p "Enter your choice (1-5): " choice
    
    case $choice in
        1)
            deploy_netlify
            ;;
        2)
            deploy_render
            ;;
        3)
            deploy_netlify
            deploy_render
            ;;
        4)
            setup_github_secrets
            ;;
        5)
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid choice. Please try again."
            show_menu
            ;;
    esac
}

# Check if running interactively
if [ -t 0 ]; then
    show_menu
else
    # Non-interactive mode - deploy to both
    deploy_netlify
    deploy_render
fi
