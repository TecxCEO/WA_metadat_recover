import os
import re
from PIL import Image

def hybrid_extract(file_path):
    """Performs both binary and pixel-level LSB scanning."""
    findings = {"Binary_Links": [], "LSB_Preview": "None"}

    # 1. BINARY SCAN: Search for hidden URLs in raw file bytes
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            # Regex to find standard URL patterns
            url_pattern = re.compile(rb'https?://[^\s\'"<>]+')
            binary_links = url_pattern.findall(content)
            findings["Binary_Links"] = [link.decode('utf-8', errors='ignore') for link in binary_links]
    except Exception:
        pass

    # 2. LSB SCAN: Extract the least significant bits from the first 500 pixels
    try:
        img = Image.open(file_path).convert('RGB')
        pixels = img.load()
        width, height = img.size
        
        bit_stream = ""
        count = 0
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                # Collect the last bit of each RGB channel
                bit_stream += f"{r&1}{g&1}{b&1}"
                count += 1
                if count > 500: break
            if count > 500: break
            
        # Convert bits to characters
        chars = [chr(int(bit_stream[i:i+8], 2)) for i in range(0, len(bit_stream), 8) if len(bit_stream[i:i+8]) == 8]
        # Filter for printable text
        findings["LSB_Preview"] = "".join([c for c in chars if c.isprintable()])[:50]
    except Exception:
        pass

    return findings

def scan_folder(folder_path):
    """Iterates through all images in a folder and prints found data."""
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found.")
        return

    print(f"{'File Name':<30} | {'Links Found':<12} | {'LSB Text Preview'}")
    print("-" * 80)

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                full_path = os.path.join(root, file)
                data = hybrid_extract(full_path)
                
                links_count = len(data["Binary_Links"])
                lsb_text = data["LSB_Preview"]
                
                print(f"{file[:30]:<30} | {links_count:<12} | {lsb_text}")
                
                if links_count > 0:
                    for link in data["Binary_Links"]:
                        print(f"   [!] Found URL: {link}")

# --- Set your path here ---
# Use 'r' before the string to handle backslashes correctly
TARGET_DIR = r"C:\Users\TecX's CTO\Downloads"
scan_folder(TARGET_DIR)
