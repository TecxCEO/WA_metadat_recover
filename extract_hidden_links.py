import os
import re
from PIL import Image
from PIL.ExifTags import TAGS

def extract_hidden_links(file_path):
    if not os.path.exists(file_path):
        return "File not found."

    found_data = {
        "Metadata_Links": [],
        "Binary_Appended_Links": []
    }

    # 1. SCAN METADATA (EXIF/XMP)
    try:
        img = Image.open(file_path)
        exif = img.getexif()
        if exif:
            for tag_id, value in exif.items():
                tag_name = TAGS.get(tag_id, tag_id)
                # Look for strings containing 'http' or 'www'
                if isinstance(value, str) and ("http" in value.lower() or "www" in value.lower()):
                    found_data["Metadata_Links"].append(f"{tag_name}: {value}")
    except Exception as e:
        found_data["Metadata_Links"].append(f"Metadata scan error: {e}")

    # 2. SCAN RAW BINARY (For appended data/Steganography)
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            # Regex to find standard URL patterns in bytes
            url_pattern = rb'https?://[^\s\'"<>]+'
            binary_links = re.findall(url_pattern, content)
            # Convert bytes back to readable text
            found_data["Binary_Appended_Links"] = [link.decode('utf-8', errors='ignore') for link in binary_links]
    except Exception as e:
        found_data["Binary_Appended_Links"].append(f"Binary scan error: {e}")

    return found_data

if __name__=="__main__":
    # --- Example Usage ---
    # Path to your WhatsApp Images folder
    folder_path = r"C:\Users\TecX's CTO\Downloads"
    # Example file
    img=["1000034148.jpg", "1000034352.jpg", "1000034334.jpg", "1000034378.jpg", "1000034398.jpg", "Mr. Rahul. invoice.pdf"]
    for i in range(len(img)):
        img_path = os.path.join(folder_path, img[i])
        # --- HOW TO RUN --
        # path = r"C:\Users\TecX's CTO\Downloads\image_name.jpg" # Use 'r' for paths with backslashes
        results = extract_hidden_links(img_path)
        print(results)
