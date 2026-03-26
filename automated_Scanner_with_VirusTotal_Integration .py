import os
import re
import csv
import time
import requests
from PIL import Image

# --- CONFIGURATION ---
VT_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual key
TARGET_DIR = r"C:\Users\TecX's CTO\Downloads"
OUTPUT_FILE = "security_scan_with_vt.csv"

def check_url_vt(url):
    """Queries VirusTotal for a URL's reputation."""
    if not VT_API_KEY or VT_API_KEY == "YOUR_API_KEY_HERE":
        return "No API Key"
        
    vt_url = "https://www.virustotal.com"
    headers = {"x-apikey": VT_API_KEY}
    
    try:
        # Step 1: Submit URL for analysis
        response = requests.post(vt_url, data={"url": url}, headers=headers)
        if response.status_code == 429: return "Rate limit exceeded"
        if response.status_code != 200: return f"Error {response.status_code}"
        
        # Step 2: Get report (using the ID from submission)
        analysis_id = response.json()['data']['id']
        report_url = f"https://www.virustotal.com{analysis_id}"
        
        # Give VT a few seconds to process
        time.sleep(2) 
        report = requests.get(report_url, headers=headers).json()
        stats = report['data']['attributes']['stats']
        
        return f"Malicious: {stats['malicious']}, Harmless: {stats['harmless']}"
    except Exception as e:
        return f"Scan failed: {e}"

def hybrid_extract(file_path):
    """Scans for links and LSB data."""
    findings = {"Links": [], "LSB": "None"}
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            urls = re.findall(rb'https?://[^\s\'"<>]+', content)
            findings["Links"] = list(set([u.decode('utf-8', errors='ignore') for u in urls]))
    except: pass
    return findings

def run_full_scan():
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['File Name', 'URL Found', 'VirusTotal Result']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for root, _, files in os.walk(TARGET_DIR):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    full_path = os.path.join(root, file)
                    data = hybrid_extract(full_path)
                    
                    if not data["Links"]:
                        writer.writerow({'File Name': file, 'URL Found': 'None', 'VirusTotal Result': 'N/A'})
                    
                    for link in data["Links"]:
                        print(f"Scanning {link} from {file}...")
                        result = check_url_vt(link)
                        writer.writerow({
                            'File Name': file,
                            'URL Found': link,
                            'VirusTotal Result': result
                        })
                        # Wait to respect free API rate limits (4 per minute)
                        time.sleep(15) 

    print(f"Full report saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    run_full_scan()
