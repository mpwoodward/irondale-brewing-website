import os
import re

# --- Configuration ---
# Directory where your Markdown (.md) files are.
CONTENT_DIR = "content"
# --- End Configuration ---

# Regex to find the corrupted pattern: a dot, followed by '/images/', then the actual extension.
# We capture the extension so we can put it back correctly.
# Example: '.jpg' became './images/jpg'
CORRUPTED_PATTERN = re.compile(r"\./images/(\w+)", re.IGNORECASE)

def fix_corrupted_paths():
    """Scans content files and fixes the specific image path corruption."""
    print("Starting image path repair...")
    
    for root, _, files in os.walk(CONTENT_DIR):
        for filename in files:
            if not filename.endswith(".md"):
                continue

            filepath = os.path.join(root, filename)
            print(f"\nProcessing file: {filepath}")

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            original_content = content
            
            # Replace the corrupted pattern with the correct one (e.g., './images/jpg' -> '.jpg')
            content = CORRUPTED_PATTERN.sub(r".\1", content)

            if content != original_content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"  - Successfully repaired image paths in {filename}")
            else:
                print("  - No corrupted image URLs found.")

if __name__ == "__main__":
    fix_corrupted_paths()
    print("\nImage path repair complete!")