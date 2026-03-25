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

# Usage
# result = get_image_metadata("IMG-20231020-WA0005.jpg")
# print(result)

