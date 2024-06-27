import base64
import requests
import csv
import pandas as pd
from io import BytesIO
from PIL import Image
import os
from imgcat import imgcat
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI

load_dotenv()
azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
azure_oai_key = os.getenv("AZURE_OAI_KEY")
azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")

def download_image(url):
    response = requests.get(url)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))

def encode_image(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def get_caption(client, base64_image, description, attributes, azure_oai_deployment):
    custom_prompt = (
        f"Enhance the following description with more detail, taking into account the given attributes:\n\n"
        f"Description: {description}\n\n"
        f"Attributes: {attributes}"
    )

    try:
        response = client.chat.completions.create(
            model=azure_oai_deployment,
            temperature=0.7,
            max_tokens=4096,
            messages=[
                {"role": "system", "content": custom_prompt},
                {"role": "user", "content": f"data:image/jpeg;base64,{base64_image}"}
            ]
        )
        if response.choices:
            caption = response.choices[0].message["content"].strip()
            return caption
    except Exception as e:
        print(f"API request failed: {e}")
    return "Failed to get caption"

def process_catalog(dataframe, output_csv, client, azure_oai_deployment):
    with open(output_csv, mode='w', newline='') as outfile:
        fieldnames = list(dataframe.columns) + ['detailed_caption']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for index, row in dataframe.iterrows():
            try:
                image = download_image(row['img'])
                base64_image = encode_image(image)
                attributes = row['p_attributes']
                detailed_caption = get_caption(client, base64_image, row['description'], attributes, azure_oai_deployment)
                imgcat(image)
                print(f"Detailed Caption: {detailed_caption}\n")
                row['detailed_caption'] = detailed_caption
                writer.writerow(row.to_dict())
            except Exception as e:
                print(f"Failed to process row {index}: {e}")

def main():
    load_dotenv()
    input_csv = '/mnt/d/dataset.csv'
    output_csv = '/mnt/d/detailed_captions.csv'


    if not azure_oai_endpoint or not azure_oai_key or not azure_oai_deployment:
        raise ValueError("One or more environment variables (AZURE_OAI_ENDPOINT, AZURE_OAI_KEY, AZURE_OAI_DEPLOYMENT) are missing.")
    
    # Initialize the Azure OpenAI client
    client = AzureOpenAI(
        azure_endpoint = azure_oai_endpoint, 
        api_key=azure_oai_key,  
        api_version="2024-02-15-preview"
    )

    dataframe = pd.read_csv(input_csv)
    process_catalog(dataframe, output_csv, client, azure_oai_deployment)
    print("Processing complete. Detailed captions saved to", output_csv)

if __name__ == "__main__":
    main()
