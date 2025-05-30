import os
import json
from datetime import datetime, timezone
from slugify import slugify
import openai
import base64
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- CONFIG ---
KEYWORDS = [
    "Best crypto trading bots Australia 2025",
    "AI bots for crypto day trading",
    "Automated crypto tools",
    "Top crypto trading bots for beginners",
    "Crypto trading automation platforms",
    "Best AI crypto trading software 2025",
    "Pionex vs 3Commas comparison",
    "Cryptohopper review 2025",
    "How to use AI for crypto trading",
    "Crypto trading bots for Binance"
]
AFFILIATE_LINKS = {
    "Pionex": "https://www.pionex.com/en/signUp?r=0fbHusbhVhc",
    "3Commas": "https://app.3commas.io/auth/registration?utm_source=referral&utm_medium=cabinet&c=tc1676699",
    "Cryptohopper": "https://www.cryptohopper.com/?atid=38457"
}
POSTS_DIR = "content/posts/"
TRACK_FILE = "data/published.json"
IMAGES_DIR = "images/"

# --- OPENAI SETUP ---
def setup_openai():
    """Initialize OpenAI client with API key from environment variables."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.\n"
            "Export it in your shell: export OPENAI_API_KEY='your-api-key-here'"
        )
    openai.api_key = api_key
    print("OpenAI API key loaded from environment variables.")

# --- HELPERS ---
def ensure_dirs():
    print("Ensuring directories exist...")
    # Change to project root directory (parent of scripts)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    print(f"Working directory: {os.getcwd()}")
    
    os.makedirs(POSTS_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    os.makedirs("data", exist_ok=True)

def load_published():
    print(f"Loading published posts from {TRACK_FILE}...")
    if not os.path.exists(TRACK_FILE):
        return set()
    with open(TRACK_FILE, "r") as f:
        return set(json.load(f))

def save_published(published):
    print(f"Saving published posts to {TRACK_FILE}...")
    with open(TRACK_FILE, "w") as f:
        json.dump(list(published), f)

def render_markdown(title, meta, body, tags, image_url, affiliate_callout):
    date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    slug = slugify(title)
    frontmatter = f"""---
title: \"{title}\"
date: {date}
tags: {tags}
meta: \"{meta}\"
image: {image_url}
schema: Article
description: \"{meta}\"
---
"""
    disclaimer = "**Disclaimer: This post contains affiliate links.**"
    toc = "## Table of Contents\n- [Introduction](#introduction)\n- [Main Content](#main-content)\n- [Conclusion](#conclusion)"
    return f"{frontmatter}\n{toc}\n\n{affiliate_callout}\n\n{body}\n\n{disclaimer}\n"

def pick_affiliate_links(text):
    links = []
    for name, url in AFFILIATE_LINKS.items():
        if name.lower() in text.lower():
            links.append(f"[**Try {name} for Free**]({url})")
    if not links:
        # fallback: pick 1-2 random
        import random
        links = [f"[**Try {name} for Free**]({url})" for name, url in random.sample(list(AFFILIATE_LINKS.items()), 2)]
    return "\n\n".join(links)

def call_gpt4_for_post(keyword):
    prompt = f"""
You are an expert crypto/AI tools blogger. Write a fully SEO-optimized blog post for the keyword: '{keyword}'.

Return your response as strict JSON with these fields:
- title: (string, catchy, 2025-focused)
- meta: (SEO meta description, 155 chars max)
- body: (Markdown, 5+ paragraphs, with H2/H3s, internal links, and 1-2 affiliate callouts like [**Try 3Commas for Free**](https://app.3commas.io/auth/registration?utm_source=referral&utm_medium=cabinet&c=tc1676699))
- image_prompt: (short DALL·E prompt for a blog hero image)

Add a Table of Contents, schema.org Article JSON-LD, and a disclaimer at the end: "This post contains affiliate links."
"""
    print(f"Calling GPT-4 for keyword: {keyword}")
    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1200
        )
        content = response.choices[0].message.content
        print(f"GPT-4 response received for '{keyword}'.")
        import json as pyjson
        data = pyjson.loads(content)
        return data
    except Exception as e:
        print(f"OpenAI API error for '{keyword}': {e}")
        return None

def generate_dalle_image(prompt, slug):
    print(f"Generating DALL·E image for slug: {slug} with prompt: {prompt}")
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response.data[0].url
        print(f"DALL·E image URL: {image_url}")
        # Download the image and save locally
        img_data = requests.get(image_url).content
        img_path = os.path.join(IMAGES_DIR, f"{slug}.png")
        with open(img_path, "wb") as handler:
            handler.write(img_data)
        print(f"Image saved to {img_path}")
        return f"/images/{slug}.png"
    except Exception as e:
        print(f"DALL·E error for '{slug}': {e}")
        return "/images/placeholder.png"

def generate_post(keyword):
    print(f"Generating post for keyword: {keyword}")
    data = call_gpt4_for_post(keyword)
    slug = slugify(keyword)
    if not data:
        print(f"Falling back to placeholder content for '{keyword}'")
        title = keyword
        meta = f"SEO meta description for {keyword}"
        body = f"### Introduction\n\nThis is an AI-generated article about {keyword}.\n\n### Main Content\n\n- Overview of {keyword}\n- Benefits of using crypto trading bots\n- How to choose the best bot\n- Security and risks\n- Final thoughts\n\n### Conclusion\n\nExplore the best crypto trading bots and tools for 2025."
        image_url = "/images/placeholder.png"
    else:
        title = data.get("title", keyword)
        meta = data.get("meta", f"SEO meta description for {keyword}")
        body = data.get("body", f"### Introduction\n\nThis is an AI-generated article about {keyword}.")
        image_prompt = data.get("image_prompt", f"crypto trading bots, futuristic, 2025, digital art")
        image_url = generate_dalle_image(image_prompt, slug)
    affiliate_callout = pick_affiliate_links(keyword)
    tags = ["crypto", "trading", "bots", "AI", "2025"]
    print(f"Rendering markdown for '{keyword}'...")
    return render_markdown(title, meta, body, tags, image_url, affiliate_callout)

def main():
    ensure_dirs()
    published = load_published()
    new_posts = 0
    for kw in KEYWORDS:
        slug = slugify(kw)
        if slug in published:
            print(f"Skipping already published: {kw}")
            continue
        print(f"Starting generation for: {kw}")
        md = generate_post(kw)
        post_path = f"{POSTS_DIR}{slug}.md"
        try:
            with open(post_path, "w") as f:
                f.write(md)
            print(f"Post written to {post_path}")
            published.add(slug)
            new_posts += 1
        except Exception as e:
            print(f"Error writing post for '{kw}': {e}")
    save_published(published)
    print(f"Generated {new_posts} new posts.")

if __name__ == "__main__":
    setup_openai()
    main() 