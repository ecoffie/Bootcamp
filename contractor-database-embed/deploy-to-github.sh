#!/bin/bash

# Federal Contractor Database - GitHub Pages Deployment Script

echo "🚀 Federal Contractor Database - GitHub Pages Deploy"
echo "=================================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: Federal contractor database"
    echo "✅ Git repository initialized"
    echo ""
else
    echo "✅ Git repository already exists"
    echo ""
fi

# Check if remote exists
if git remote get-url origin &> /dev/null; then
    echo "✅ Remote 'origin' already configured"
    REMOTE_URL=$(git remote get-url origin)
    echo "   URL: $REMOTE_URL"
    echo ""
else
    echo "⚠️  No remote repository configured"
    echo ""
    echo "Please follow these steps:"
    echo "1. Go to https://github.com/new"
    echo "2. Create a new repository named 'contractor-database'"
    echo "3. Do NOT initialize with README, .gitignore, or license"
    echo "4. Copy the repository URL (e.g., https://github.com/username/contractor-database.git)"
    echo ""
    read -p "Enter your GitHub repository URL: " REPO_URL

    if [ -z "$REPO_URL" ]; then
        echo "❌ No URL provided. Exiting."
        exit 1
    fi

    echo ""
    echo "📡 Adding remote repository..."
    git remote add origin "$REPO_URL"
    echo "✅ Remote added"
    echo ""
fi

# Ensure we're on main branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "🔄 Switching to main branch..."
    git branch -M main
fi

# Add any new changes
echo "📝 Checking for changes..."
if [[ -n $(git status -s) ]]; then
    echo "📦 Adding new changes..."
    git add .
    git commit -m "Update contractor database - $(date +%Y-%m-%d)"
    echo "✅ Changes committed"
else
    echo "✅ No changes to commit"
fi
echo ""

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully deployed to GitHub!"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Go to your GitHub repository"
    echo "2. Click 'Settings' → 'Pages'"
    echo "3. Under 'Source', select 'main' branch"
    echo "4. Click 'Save'"
    echo "5. Wait 2-3 minutes for deployment"
    echo ""
    echo "Your database will be available at:"

    # Extract username and repo from URL
    REMOTE_URL=$(git remote get-url origin)
    if [[ $REMOTE_URL =~ github.com[:/]([^/]+)/([^/.]+) ]]; then
        USERNAME="${BASH_REMATCH[1]}"
        REPO="${BASH_REMATCH[2]}"
        echo "https://${USERNAME}.github.io/${REPO}/"
    else
        echo "(Check GitHub Pages settings for your URL)"
    fi
    echo ""
else
    echo ""
    echo "❌ Push failed. Common issues:"
    echo "1. Make sure you've created the repository on GitHub"
    echo "2. Check that your GitHub credentials are configured"
    echo "3. Verify the repository URL is correct"
    echo ""
    echo "Try running: git push -u origin main"
fi
