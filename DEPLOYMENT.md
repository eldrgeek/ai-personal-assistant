# 🚀 Deployment Guide - Netlify + Render

This guide will help you deploy your AI Personal Assistant to production using Netlify (frontend) and Render (backend) with automatic deployment via GitHub Actions.

## 📋 Prerequisites

- ✅ Netlify CLI installed and logged in
- ✅ Render CLI installed and logged in
- ✅ GitHub repository with push access
- ✅ Node.js 18+ and Python 3.11+

## 🌐 Step 1: Deploy Frontend to Netlify

### 1.1 Create Netlify Site
```bash
# Navigate to your project
cd frontend

# Create a new Netlify site
netlify sites:create --name ai-personal-assistant

# Note down the Site ID and URL from the output
```

### 1.2 Get Netlify Auth Token
1. Go to [Netlify User Settings](https://app.netlify.com/user/applications#personal-access-tokens)
2. Click "New access token"
3. Give it a name (e.g., "GitHub Actions")
4. Copy the token (you'll need this for GitHub secrets)

### 1.3 Test Netlify Deployment
```bash
# Build and deploy
npm run build
netlify deploy --prod --dir=dist

# Verify the deployment
netlify open
```

## ☁️ Step 2: Deploy Backend to Render

### 2.1 Create Render Service
```bash
# Navigate to your project root
cd ..

# Deploy using render.yaml
render deploy
```

### 2.2 Get Render Webhook URL
1. Go to your Render dashboard
2. Select your service
3. Go to "Settings" → "Webhooks"
4. Create a new webhook for "Deploy"
5. Copy the webhook URL

### 2.3 Test Render Deployment
```bash
# Check service status
render ps

# View logs
render logs
```

## 🔑 Step 3: Configure GitHub Secrets

### 3.1 Add Repository Secrets
1. Go to your GitHub repository
2. Navigate to "Settings" → "Secrets and variables" → "Actions"
3. Add the following secrets:

| Secret Name | Value | Source |
|-------------|-------|---------|
| `NETLIFY_AUTH_TOKEN` | Your Netlify auth token | Netlify User Settings |
| `NETLIFY_SITE_ID` | Your Netlify site ID | Netlify site dashboard |
| `RENDER_WEBHOOK_URL` | Your Render webhook URL | Render service webhooks |

### 3.2 Secret Values
- **NETLIFY_AUTH_TOKEN**: `ntl_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- **NETLIFY_SITE_ID**: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- **RENDER_WEBHOOK_URL**: `https://api.render.com/webhook/v2/...`

## 🚀 Step 4: Test Automatic Deployment

### 4.1 Push to Main Branch
```bash
# Make a small change
echo "# Updated at $(date)" >> README.md

# Commit and push
git add .
git commit -m "Test automatic deployment"
git push origin main
```

### 4.2 Monitor GitHub Actions
1. Go to your GitHub repository
2. Click "Actions" tab
3. Watch the deployment workflow run
4. Check both Netlify and Render for successful deployments

## 🔧 Step 5: Update Configuration

### 5.1 Update CORS Settings
After deployment, update the CORS origins in `backend/main.py`:

```python
# Production CORS settings
allow_origins=[
    "https://your-actual-netlify-site.netlify.app",
    "https://your-actual-render-app.onrender.com"
],
```

### 5.2 Update Frontend API URLs
Update the API base URL in your frontend components to use your Render backend URL.

## 📱 Step 6: Test Production Deployment

### 6.1 Test Frontend
- Visit your Netlify URL
- Verify all components load correctly
- Test the UI functionality

### 6.2 Test Backend
- Visit your Render URL + `/health`
- Test API endpoints
- Verify CORS is working

### 6.3 Test Integration
- Test frontend-backend communication
- Verify data flows correctly
- Check for any CORS or authentication issues

## 🛠️ Manual Deployment (Alternative)

If you prefer manual deployment, use the deployment script:

```bash
# Make executable and run
chmod +x deploy.sh
./deploy.sh
```

## 🔍 Troubleshooting

### Common Issues

#### 1. CORS Errors
- Verify CORS origins in backend configuration
- Check that frontend URL is included in allowed origins

#### 2. Build Failures
- Check Node.js version (should be 18+)
- Verify all dependencies are installed
- Check for TypeScript compilation errors

#### 3. Deployment Failures
- Verify GitHub secrets are correct
- Check Render service logs
- Ensure webhook URLs are valid

#### 4. Environment Variables
- Verify all required environment variables are set
- Check that production settings are correct
- Ensure database URLs are accessible

### Debug Commands
```bash
# Check Netlify status
netlify status

# Check Render status
render ps

# View Render logs
render logs

# Test GitHub Actions locally (if using act)
act push
```

## 📊 Monitoring & Maintenance

### 1. Health Checks
- Backend: `https://your-render-app.onrender.com/health`
- Frontend: Monitor Netlify analytics

### 2. Logs
- Netlify: Built-in logging and analytics
- Render: Service logs in dashboard
- GitHub Actions: Workflow logs

### 3. Updates
- Push to main branch triggers automatic deployment
- Monitor deployment status in GitHub Actions
- Test changes in development before pushing

## 🎯 Next Steps

After successful deployment:

1. **Set up custom domain** (optional)
2. **Configure SSL certificates** (automatic with Netlify/Render)
3. **Set up monitoring and alerts**
4. **Implement database backups**
5. **Add CI/CD pipeline enhancements**

## 🎉 Success!

Your AI Personal Assistant is now deployed to production with:
- ✅ **Frontend**: Netlify with automatic builds
- ✅ **Backend**: Render with automatic deployments
- ✅ **CI/CD**: GitHub Actions for seamless updates
- ✅ **Monitoring**: Health checks and logging

**Every push to main branch now automatically deploys your updates!** 🚀

---

*For support, check the GitHub repository issues or refer to Netlify/Render documentation.*
