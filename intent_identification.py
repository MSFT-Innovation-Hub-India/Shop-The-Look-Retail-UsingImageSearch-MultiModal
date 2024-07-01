
import os
from openai import AzureOpenAI
import dotenv

dotenv.load_dotenv()

api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OAI_DEPLOYMENT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = os.getenv("AZURE_OAI_API_VERSION")



def identify_intent(user_text, img_url):

    client = AzureOpenAI(
        api_key = api_key,
        api_version = api_version,
        base_url = f"{api_base}/openai/deployments/{deployment_name}",
    )

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            { "role": "system", "content": "You are an expert in fashion design. Based on the users intent,\
              generate a prompt that would be useful as a search query in a vector database"},

            { "role": "user", "content": [  
                { 
                    "type": "text", 
                    "text": user_text
                },
                { 
                    "type": "image_url",
                    "image_url": {
                        "url": img_url
                    }
                }
            ] } 
        ],
        max_tokens=2000 
    )

    return response.choices[0].message.content

