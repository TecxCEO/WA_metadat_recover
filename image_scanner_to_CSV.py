import os
import re
import csv
from PIL import Image

def hybrid_extract(file_path):
    """Scans for appended links and pixel-level bits."""
    findings = {"Binary_Links": [], "LSB_Preview": "None"}
    
    # 1. Binary Scan (Appended links)
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            url_pattern = re.compile(rb'https?://[^\s\'"<>]+')
            binary_links = url_pattern.findall(content)
            findings["Binary_Links"] = [link.decode('utf-8', errors='ignore') for link in binary_links]
    except: pass

    # 2. LSB Scan (Pixel-level text)
    try:
        img = Image.open(file_path).convert('RGB')
        pixels = img.load()
        width, height = img.size
        bit_stream = ""
        count = 0
        for y in range(min(height, 50)): # Scan a small sample area
            for x in range(min(width, 50)):
                r, g, b = pixels[x, y]
                bit_stream += f"{r&1}{g&1}{b&1}"
                count += 1
                if count > 500: break
            if count > 500: break
        
        # Convert bits to readable characters
        chars = [chr(int(bit_stream[i:i+8], 2)) for i in range(0, len(bit_stream), 8) if len(bit_stream[i:i+8]) == 8]
        findings["LSB_Preview"] = "".join([c for c in chars if c.isprintable()])[:50]
    except: pass
    
    return findings

def scan_to_csv(folder_path, output_csv):
    """Walks through folder and writes all results to a CSV."""
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['File Name', 'Full Path', 'Binary Links Found', 'LSB Preview']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    full_path = os.path.join(root, file)
                    data = hybrid_extract(full_path)
                    writer.writerow({
                        'File Name': file,
                        'Full Path': full_path,
                        'Binary Links Found': "; ".join(data["Binary_Links"]),
                        'LSB Preview': data["LSB_Preview"]
                    })
    print(f"Scan complete. Results saved to: {output_csv}")

# --- Set your specific paths here ---
TARGET_DIR = r"C:\Users\TecX's CTO\Downloads"
OUTPUT_FILE = "whatsapp_image_security_scan.csv"

scan_to_csv(TARGET_DIR, OUTPUT_FILE)
