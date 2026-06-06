# Vercel Deployment Guide

## Deployment Steps

### 1. Prepare Your Frontend

Make sure your frontend is ready:
```bash
cd frontend
npm install
npm run build
```

### 2. Deploy to Vercel

#### Option A: Using Vercel CLI
```bash
# Install Vercel CLI globally
npm i -g vercel

# Login to your Vercel account
vercel login

# Deploy
vercel
```

#### Option B: Using GitHub Integration
1. Push your code to GitHub
2. Go to [Vercel Dashboard](https://vercel.com)
3. Click "New Project"
4. Import your GitHub repository
5. Select the `frontend` directory as root
6. Deploy

### 3. Environment Variables

Set these in your Vercel project settings:

**Project Settings → Environment Variables:**
```
NEXT_PUBLIC_API_URL=https://your-api-domain.com
```

### 4. Configuration Files

The following files are already configured:
- ✅ `vercel.json` - Build configuration
- ✅ `.vercelignore` - Ignore files during deployment
- ✅ `package.json` - Updated with `vercel-build` script

## Troubleshooting

### Build Error: Exit Code 1

**Solution 1: Clear npm cache**
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
npm run build
```

**Solution 2: Check for TypeScript errors**
```bash
npx tsc --noEmit
```

**Solution 3: Verify all dependencies are installed**
```bash
npm install --legacy-peer-deps
```

### CORS Issues in Production

Update your backend CORS configuration for your Vercel domain:
```python
# In your backend (app/main.py)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-frontend.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Environment Variables Not Working

1. Verify `NEXT_PUBLIC_` prefix is used for client-side variables
2. Redeploy after adding environment variables
3. Check `.env.local` is in `.gitignore` (don't commit secrets)

## Build Optimization

### Next.js Optimization
```bash
# Analyze bundle size
npm install --save-dev @next/bundle-analyzer
```

### Performance Tips
- Use Image Optimization: `next/image`
- Enable Static Generation where possible
- Code split with dynamic imports

## Monitoring & Analytics

- **Vercel Analytics**: Automatically enabled
- **Web Vitals**: Tracked in Vercel dashboard
- **Build Logs**: Available in Vercel dashboard

## Rolling Back

If you need to revert to a previous deployment:

1. Go to Vercel Dashboard
2. Select your project
3. Go to "Deployments"
4. Click the three dots on the previous deployment
5. Select "Promote to Production"

## Custom Domain

1. Go to Project Settings → Domains
2. Add your custom domain
3. Update DNS records (Vercel will provide instructions)
4. DNS propagation may take 24-48 hours

## Production Best Practices

1. **Enable Preview Deployments**
   - Settings → Git → Preview Deployments
   - Set to automatic for all branches

2. **Set Branch Protection**
   - Settings → Git → Deployment Branches
   - Add branch rules

3. **Enable Analytics**
   - Settings → Analytics
   - Monitor real user metrics

4. **Configure Error Tracking**
   - Integrate Sentry or similar
   - Monitor production errors

## API Integration

Update your `.env.local` for production:

```env
# Development
NEXT_PUBLIC_API_URL=http://localhost:8000

# Production (set in Vercel dashboard)
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

## Troubleshooting Checklist

- [ ] `package.json` has `vercel-build` script
- [ ] All dependencies are in `package.json`
- [ ] No TypeScript errors (`npm run lint`)
- [ ] Build succeeds locally (`npm run build`)
- [ ] Environment variables set in Vercel dashboard
- [ ] Backend CORS configured for your Vercel domain
- [ ] Git repository is clean and up to date

## Support

For more help:
- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Deployment Guide](https://nextjs.org/docs/deployment)
- [Vercel GitHub Issues](https://github.com/vercel/vercel/issues)
