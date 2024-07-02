
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
    
    if img_url is not None:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                { "role": "system", "content": "You are an expert in fashion design. Based on the users intent,\
                generate a prompt that would be useful as a search query in a vector database. Unless otherwise specified, provide details \
                of color, style and material. Provide these details in 5 or more bullet points"},

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
                ] },
                {
                    "role": "assistant",
                    "content":
                        "Red women's shirt with ruffled and asymmetric hem, tie-front design, sleeveless, flowy fabric\
                         - Category: Women's Shirt \
                         - Style: Halter neck \
                         - Style: Sleeveless \
                         - Color: Bright Red \
                         - Features: Flowy, tie-knot, ruffles "
                }
            ],
            max_tokens=2000 
        )
    else:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                { "role": "system", "content": "You are an expert in fashion design. You will receive a prompt from the user.\
                    The prompt may be a follow up to previous search result or a completely new question. Any questions about the material or style can be considered\
                    a follow up question. For example 'What is the material of the first result?' Any question asking for a new item to be searched \
                    can be considered a new question. For example 'Find me a dress for summer in yellow color.' \
                    If it is a new question, generate a prompt that would be useful in a vector search. \
                    If it is a follow up question, return the following statement exactly: \"This is a follow up\""},

                { "role": "user", "content": [  
                    { 
                        "type": "text", 
                        "text": user_text
                    },
                ] }, 
            ],
            max_tokens=2000 
        )
        

    return response.choices[0].message.content
