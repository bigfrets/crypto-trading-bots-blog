# Crypto Trading Bots AI Affiliate Blog (2025)

A fully automated, SEO-optimized affiliate blog for crypto trading tools and bots. Generates daily posts using GPT-4, inserts affiliate links, and deploys to a Hugo static site.

## Features
- Auto-generates 3–5 SEO blog posts per day
- GPT-4 for content, DALL·E for images (or placeholders)
- Affiliate links and AdSense/Ezoic support
- Markdown output for Hugo static site
- Deployable to Vercel/Netlify
- Tracks published posts to avoid duplicates

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy the example environment file and add your OpenAI API key:
```bash
cp env.example .env
```

Edit `.env` and add your OpenAI API key:
```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
```

Get your API key from: https://platform.openai.com/api-keys

### 3. Export Environment Variables
For the current session:
```bash
export OPENAI_API_KEY=sk-your-actual-api-key-here
```

Or source your `.env` file if you have a tool like `python-dotenv` installed.

### 4. Test Your Setup (Recommended)
Before running the main generator, test your environment setup:
```bash
python test_env.py
```

### 5. Run the Generator
```bash
python scripts/generate_posts.py
```

## Directory Structure
```
content/posts/      # Markdown blog posts
images/             # AI-generated images
scripts/            # Automation scripts
data/published.json # Tracks published posts
env.example         # Environment variables template
test_env.py         # Test environment setup
.gitignore          # Git ignore file
```

## Deployment
- Use Hugo to build and deploy to Vercel/Netlify.
- Set up a daily cron job or scheduler for full automation. 