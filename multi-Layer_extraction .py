import os
import re
from PIL import Image

def hybrid_extract(file_path):
    if not os.path.exists(file_path):
        return "File not found."

    findings = {"Binary_Scan": [], "LSB_Scan_Preview": ""}

    # 1. BINARY SCAN (Detects appended links/text)
    # Hackers often append data after the 'End of File' marker.
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            url_pattern = rb'https?://[^\s\'"<>]+'
            found_urls = re.findall(url_pattern, content)
            findings["Binary_Scan"] = [url.decode('utf-8', errors='ignore') for url in found_urls]
    except Exception as e:
        findings["Binary_Scan"] = [f"Error: {e}"]

    # 2. LSB SCAN (Detects pixel-level hidden data)
    # Extracts the last bit of each RGB channel to find hidden ASCII text.
    try:
        img = Image.open(file_path).convert('RGB')
        pixels = img.load()
        width, height = img.size
        
        extracted_bits = ""
        # We scan the first 1000 pixels as a sample for preview
        count = 0
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                extracted_bits += str(r & 1) + str(g & 1) + str(b & 1)
                count += 1
                if count > 1000: break
            if count > 1000: break
            
        # Convert bit-stream to characters
        chars = []
        for i in range(0, len(extracted_bits), 8):
            byte = extracted_bits[i:i+8]
            if len(byte) == 8:
                chars.append(chr(int(byte, 2)))
        
        findings["LSB_Scan_Preview"] = "".join(chars)
    except Exception as e:
        findings["LSB_Scan_Preview"] = f"LSB Error: {e}"

    return findings

# Usage:
# path = r"C:\Users\TecX's CTO\Downloads\suspicious_image.png"
# print(hybrid_extract(path))
