#!/usr/bin/env python3
"""
Update affiliate links across all content files.
Run this after you get your real affiliate IDs from each platform.
"""

import os
import re
from pathlib import Path

# Update these with your actual affiliate IDs
AFFILIATE_IDS = {
    "pionex": "42671867",
    "3commas": "1676699", 
    "cryptohopper": "38457"
}

# Current placeholder links
PLACEHOLDER_LINKS = {
    "pionex": "https://www.pionex.com/en-US/sign/ref/affiliate-link",
    "3commas": "https://3commas.io/?c=affiliate-link",
    "cryptohopper": "https://www.cryptohopper.com/?atid=affiliate-link"
}

# New links with your affiliate IDs
NEW_LINKS = {
    "pionex": "https://www.pionex.com/en/signUp?r=0fbHusbhVhc",
    "3commas": "https://app.3commas.io/auth/registration?utm_source=referral&utm_medium=cabinet&c=tc1676699",
    "cryptohopper": "https://www.cryptohopper.com/?atid=38457"
}

def update_file(filepath):
    """Update affiliate links in a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Replace each placeholder link
    for platform, old_link in PLACEHOLDER_LINKS.items():
        new_link = NEW_LINKS[platform]
        if old_link in content:
            content = content.replace(old_link, new_link)
            print(f"  ✓ Updated {platform} link in {filepath}")
    
    # Only write if changes were made
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def update_all_content():
    """Update affiliate links in all content files."""
    print("🔗 Updating Affiliate Links...")
    print(f"\nCurrent IDs:")
    for platform, id in AFFILIATE_IDS.items():
        print(f"  {platform}: {id}")
    
    # Check if IDs are still placeholders
    if all(id.startswith("YOUR-") for id in AFFILIATE_IDS.values()):
        print("\n⚠️  WARNING: You need to update AFFILIATE_IDS with your actual IDs!")
        print("Edit this script and replace the placeholder IDs first.")
        return
    
    updated_files = 0
    
    # Update content files
    content_dir = Path("content")
    for filepath in content_dir.rglob("*.md"):
        if update_file(filepath):
            updated_files += 1
    
    # Update Python scripts
    scripts_dir = Path("scripts")
    for filepath in scripts_dir.glob("*.py"):
        if filepath.name != "update_affiliate_links.py":
            if update_file(filepath):
                updated_files += 1
    
    # Update Hugo config
    if update_file("hugo.toml"):
        updated_files += 1
    
    print(f"\n✅ Updated {updated_files} files with new affiliate links!")
    
    if updated_files > 0:
        print("\n📝 Next steps:")
        print("1. Review the changes")
        print("2. Rebuild your site: hugo")
        print("3. Deploy to see the updates live")

if __name__ == "__main__":
    update_all_content() 