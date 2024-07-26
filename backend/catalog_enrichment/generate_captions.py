import os
from openai import AzureOpenAI
import dotenv
import pandas as pd

dotenv.load_dotenv()

api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OAI_DEPLOYMENT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = os.getenv("AZURE_OAI_API_VERSION")


def gen_caption(img, p_attributes):

    client = AzureOpenAI(
        api_key = api_key,
        api_version = api_version,
        base_url = f"{api_base}/openai/deployments/{deployment_name}",
    )

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            { "role": "system", "content": "You are an expert in fashion design.\
            Generate an enticing description for the products in the image\
            make use of the attributes to describe the products. \
            The description that you generate must be such that it \
            can be easily used in a vectory search algorithm" },

            { "role": "user", "content": [  
                { 
                    "type": "text", 
                    "text": "Describe this picture" + p_attributes
                },
                { 
                    "type": "image_url",
                    "image_url": {
                        "url": img
                    }
                }
            ] } 
        ],
        max_tokens=2000 
    )

    return response.choices[0].message.content

def process_dataset(dataset_path):
    df = pd.read_csv(dataset_path)
    if 'img' not in df.columns or 'p_attributes' not in df.columns:
        raise ValueError("CSV must contain 'image_url' and 'attributes' columns")

    df['caption'] = df.apply(lambda row: gen_caption(row['img'], row['p_attributes']), axis=1)
    return df

def main():
    dataset_path = "dataset.csv"
    df = process_dataset(dataset_path)
    print(df)


if __name__ == "__main__":
    main()