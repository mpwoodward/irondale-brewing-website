import os
import re
import requests
from urllib.parse import urlparse, unquote

# --- Configuration ---
# Directory where your Markdown (.md) files are.
CONTENT_DIR = "content"
# The local directory where images should be saved. Must be in STATIC_PATHS.
LOCAL_IMAGE_DIR = os.path.join(CONTENT_DIR, "images")
# The base URL of your old WordPress site.
WP_SITE_URL = "https://irondalebrewing.com"
# --- End Configuration ---

WP_UPLOADS_PATH = "/wp-content/uploads/"
# This regex finds the full URL. It looks for the base URL, the uploads path, and then any character
# that is not a quote, parenthesis, or bracket until it finds a common image extension.
# It also handles URL-encoded characters like %22.
WP_IMAGE_URL_PATTERN = re.compile(f"({re.escape(WP_SITE_URL)}{re.escape(WP_UPLOADS_PATH)}[^\"'()\\[\\]]+?\\.(?:jpg|jpeg|png|gif|webp))", re.IGNORECASE)

def download_image(url, save_path):
    """Downloads an image from a URL and saves it to a local path."""
    if os.path.exists(save_path):
        print(f"    - Skipping, already exists: {os.path.basename(save_path)}")
        return

    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"    - Downloaded: {os.path.basename(save_path)}")
    except requests.exceptions.RequestException as e: # Catching a broader exception for network issues
        print(f"    - FAILED to download {url}: {e}")

def process_content_files():
    """Scans content files, downloads images, and updates paths."""
    print("Starting image migration...")
    
    for root, _, files in os.walk(CONTENT_DIR):
        for filename in files:
            # Process only Markdown files, you can add other extensions like .rst
            if not filename.endswith(".md"):
                continue

            filepath = os.path.join(root, filename)
            print(f"\nProcessing file: {filepath}")

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Use a set to store unique URLs found to avoid re-downloading.
            found_urls = set(WP_IMAGE_URL_PATTERN.findall(content)) 

            if not found_urls:
                print("  - No WordPress image URLs found.")
                continue
            
            print(f"  - Found {len(found_urls)} unique WordPress image URL(s).")
            original_content = content
            for url in found_urls:
                print(f"    - Processing URL: {url}")
                # Extract the path part after /wp-content/uploads/
                # unquote() handles special characters in filenames like %22
                path_part = unquote(urlparse(url).path).replace(WP_UPLOADS_PATH, "")
                
                local_save_path = os.path.join(LOCAL_IMAGE_DIR, path_part)
                # The new path to be used in the markdown file.
                new_relative_path = f"/images/{path_part}"

                download_image(url, local_save_path)

                # Replace the absolute WordPress URL with the new local path
                content = content.replace(url, new_relative_path)

            if content != original_content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"  - Successfully updated image paths in {filename}")

if __name__ == "__main__":
    process_content_files()
    print("\nMigration complete!")