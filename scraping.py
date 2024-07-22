import requests
from bs4 import BeautifulSoup
import re
import json
import os

url = "https://www2.hm.com/en_in/sale/men/view-all.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    image_urls = []
    img_tags = soup.find_all("img")
    for img in img_tags:
        if 'src' in img.attrs:
            image_urls.append(img['src'])
        if 'data-src' in img.attrs:
            image_urls.append(img['data-src'])

    style_tags = soup.find_all(style=True)
    for tag in style_tags:
        style = tag['style']
        urls = re.findall(r'url\((.*?)\)', style)
        for url in urls:
            image_urls.append(url.strip('\'"'))

    script_tags = soup.find_all("script")
    for script in script_tags:
        if script.string:
            urls = re.findall(r'(https?://[^\s]+(?:\.jpg|\.png|\.gif))', script.string)
            image_urls.extend(urls)
    
    for image_url in image_urls:
        print(image_url)
        
    # Open the file with extracted image URLs
    with open('extracted_image_urls.txt', 'r') as file:
        raw_urls = file.readlines()

    # Function to process and complete URLs
    def complete_url(url):
        url = url.strip()
        if url.startswith('//'):
            return 'https:' + url
        elif url.startswith('/'):
            return 'https://www2.hm.com' + url
        else:
            return url

    # Process URLs and ensure they are complete
    complete_urls = [complete_url(url) for url in raw_urls]

    # Save the complete URLs to a new file
    with open('complete_image_urls.txt', 'w') as file:
        for url in complete_urls:
            file.write(url + '\n')

    # Print complete URLs to verify
    for url in complete_urls:
        print(url)

else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
