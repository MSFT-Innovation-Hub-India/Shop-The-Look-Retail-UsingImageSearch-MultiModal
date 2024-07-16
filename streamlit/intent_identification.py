
import os
from openai import AzureOpenAI
import dotenv

dotenv.load_dotenv()

api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OAI_DEPLOYMENT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = os.getenv("AZURE_OAI_API_VERSION")



def identify_intent(user_text, img_url, previous_prompts, previous_intents):

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
                of color, style, gender and material. Provide these details in 5 or more bullet points. \
                Provide only the search parameters in your response. Do not say things such as 'Certainly' or 'Here are the details you requested' \
                If the user asks for a specific parameter, only mention what the parameter is and not where it came from. For example, if the user asks for the color \
                of a red tshirt, only return red, and not red tshirt"},

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
                        "- Category: Women's Shirt \
                         - Style: Halter neck \
                         - Gender: Female \
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
                { "role": "system", "content": "You purpose is to identify the intent of a user and generate a vector search query which is descriptive and allows the user to find what they are looking for in a vector database. You will receive a prompt from the user.\
                    The prompt may be a follow up to previous search result or a completely new question. Any questions about the material or style can be considered\
                    a follow up question. A follow up question can be about a previous result or image. For example 'What is the material of the first result? ' \
                    Any question asking for a new item to be searched can be considered a new question. For example 'Find me a dress for summer in yellow color.' \
                    Any question asking for a matching item can be considered a new question. For example 'Find me a matching scarf for the first result.' This should find a scarf and not return the same result. \
                    Additionally, a question asking for more or better options can be considered a new question. For example 'I need more formal options', or 'I want more options in blue'.\
                    If it is a new question, generate a prompt that would be useful in a vector search. Provide context from previous prompts and intents, such as color and style, if applicable. Provide as much detail as possible, such as color and style in a bulleted list. \
                    Remember details such as product that is being searched or purpose of the search. \
                    If it is a follow up question, return the following statement exactly: \"This is a follow up\""},

                { "role": "user", "content": [  
                    { 
                        "type": "text", 
                        "text": user_text
                    },
                ] }, 
                {
                    "role": "user", "content": previous_prompts
                },
                {
                    "role": "user", "content": previous_intents
                },
                {
                    "role":"assistant",
                    "content": '''
                        - **Context**: Formal clothing options for a weekend trip to Goa where boss will be present
                        - **Details**:
                            - Formal outfits
                            - Stylish yet appropriate for a professional setting
                            - Suitable for warm weather

                        "Formal outfits for a weekend trip to Goa, stylish and appropriate for professional setting, suitable for warm weather."'''
                    
                }
            ],
            max_tokens=2000 
        )
        

    return response.choices[0].message.content
