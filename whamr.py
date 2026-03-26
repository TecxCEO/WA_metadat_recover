import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_image_metadata(img_path):
    try:
        image = Image.open(img_path)
        exif_data = image._getexif()
        
        if not exif_data:
            return "No EXIF metadata found. WhatsApp likely stripped it."

        metadata = {}
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            
            # Extract Device/Camera Info
            if tag_name in ['Make', 'Model', 'Software']:
                metadata[tag_name] = value
                
            # Extract and Decode GPS Info
            if tag_name == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_tag = GPSTAGS.get(t, t)
                    gps_data[sub_tag] = value[t]
                metadata["GPS"] = gps_data
        
        return metadata if metadata else "Metadata exists but no GPS/Camera info found."
        
    except Exception as e:
        return f"Error: {e}"
if __name__=="__main__":
    # --- Example Usage ---
    # Path to your WhatsApp Images folder
    folder_path = r"C:\Users\TecX's CTO\Downloads"
    # Example file
    img_path = os.path.join(folder_path, "1000034148.jpg")
    # Print results
    ####metadata = get_whatsapp_file_metadata(img_path)
    # Usage
    result = get_image_metadata(img_path)
    print(result)
    for key, value in metadata.items():
        print(f"{key}: {value}")
    
