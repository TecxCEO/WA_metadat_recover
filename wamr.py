import os
import re
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

def get_whatsapp_file_metadata(file_path):
    """
    Extracts metadata from WhatsApp downloaded files.
    """
    if not os.path.exists(file_path):
        return "File not found."

    file_name = os.path.basename(file_path)
    meta = {
        "File Name": file_name,
        "System Creation Time": datetime.fromtimestamp(os.path.getctime(file_path)),
        "System Modification Time": datetime.fromtimestamp(os.path.getmtime(file_path)),
        "WhatsApp Received Date": None,
        "WhatsApp Sequential ID": None,
        "EXIF Data": {}
    }

    # 1. Extract Date from WhatsApp Filename (IMG-YYYYMMDD-WA0000.jpg)
    wa_match = re.search(r'IMG-(\d{8})-WA(\d+)', file_name)
    if wa_match:
        date_str = wa_match.group(1)
        seq_id = wa_match.group(2)
        meta["WhatsApp Received Date"] = datetime.strptime(date_str, '%Y%m%d').strftime('%Y-%m-%d')
        meta["WhatsApp Sequential ID"] = seq_id

    # 2. Extract Remaining EXIF Metadata (if any)
    try:
        img = Image.open(file_path)
        exifdata = img.getexif()
        for tagid in exifdata:
            tagname = TAGS.get(tagid, tagid)
            value = exifdata.get(tagid)
            meta["EXIF Data"][tagname] = str(value)
    except Exception as e:
        meta["EXIF Data"] = f"No EXIF data or error: {e}"

    return meta


if __name__=="__main__":
    # --- Example Usage ---
    # Path to your WhatsApp Images folder
    folder_path = r"C:\Users\TecX's CTO\Downloads"
    # Example file
    img_path = os.path.join(folder_path, "1000034148.jpg")
    # Print results
    metadata = get_whatsapp_file_metadata(img_path)
    for key, value in metadata.items():
        print(f"{key}: {value}")
    #####get_whatsapp_file_metadata(img_path)
