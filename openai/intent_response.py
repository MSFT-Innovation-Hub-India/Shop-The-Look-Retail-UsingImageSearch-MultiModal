import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv(".env")

api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OAI_DEPLOYMENT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = os.getenv("AZURE_OAI_API_VERSION")

app = Flask(__name__)
CORS(app)

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
                of color, style and material. Provide these details in 5 or more bullet points. \
                Provide only the search parameters in your response. Do not say things such as 'Certainly' or 'Here are the details you requested' \
                If the user asks for a specific parameter, only mention what the parameter is and not where it came from. For example, if the user asks for the color \
                of a red tshirt, only return red, and not red tshirt. If the user query is ambiguous, state that the user needs to be more specfic."},

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
                { "role": "system", "content": "You purpose is to identify the intent of a user and generate a vector search query which is descriptive and allows the user to find what they are looking for in a vector database. You will receive a prompt from the user.\
                    The prompt may be a follow up to previous search result or a completely new question. Any questions about the material or style can be considered\
                    a follow up question. A follow up question will ONLY be about a previous result or image. For example 'What is the material of the first result?' \
                    Any question asking for a new item to be searched can be considered a new question. For example 'Find me a dress for summer in yellow color.' \
                    Additionally, a question asking for more or better options can be considered a new question. For example 'I need more formal options', or 'I want more options in blue'.\
                    If it is a new question, generate a prompt that would be useful in a vector search. Provide context from previous prompts and intents, such as color and style, if applicable. Provide as much detail as possible, such as color and style in a bulleted list. \
                    Do not forget to provide the context from previous intents. Remember details such as product that is being searched or purpose of the search. \
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

def response_generation(response_json, prompt): 
    try: 
        # Get configuration settings 
        #load_dotenv()
        #azure_oai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        #azure_oai_key = os.getenv("AZURE_OPENAI_KEY")
       # azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")
        
        # Initialize the Azure OpenAI client...
        client = AzureOpenAI(
            azure_endpoint=api_base, 
            api_key=api_key ,  
            api_version="2024-02-15-preview"
        )

        system_message = """You are a fashion assistant which provides the user an enticing fashion suggestion,
        based on their request and the description of the suggested clothing item. You are given the user prompt as context. \
        You must use the user prompt only to make the result conversational. The remainder of the response must be based on the description of the suggested clothing item. \
        Assume this description data is the fashion suggestion, so you do not have to suggest new clothing items. \
        If there are multiple items, describe each one in a separate paragraph.
        You may provide only relevant attributes from the description data and answer the users request in a conversational manner.
        Do not give bullet points unless specifically asked. Provide a conversational and enticing paragraph description. Provide a maximum of 3 sentence description in each paragraph"""
        
        if response_json is not None:
            response = client.chat.completions.create(
                model=deployment_name,
                temperature=0.4,
                max_tokens=4096,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": response_json} ,
                    {"role": "assistant", "content": '''You're going to have such a fabulous time in Paris! Let's make sure your outfits are as picturesque as the city itself.
                    First, consider a stylish casual pullover hoodie that screams Parisian chic. Made from soft polyester fabric with a knitted weave, this hoodie is both cozy and trendy. The hooded neckline with contrasting black drawstrings adds a touch of flair, while the cropped length and straight hemline make it perfect for layering. The typography print "C'est La Vie Paris" on the front is the ultimate nod to your Parisian adventure. Pair this with your favorite jeans or a cute skirt for a casual yet stylish look that's perfect for exploring the city and snapping some Instagram-worthy photos.
                    For a laid-back yet fashionable look, these high-rise denim shorts are a must-have. Crafted from durable cotton in a trendy indigo hue, they feature a fashionable washed pattern and a practical 5-pocket configuration. The high-rise waist is flattering and perfect for pairing with tucked-in tops or cropped tees. These shorts are ideal for a casual day out, whether you're strolling along the Seine or enjoying a café au lait at a charming bistro. Plus, they're easy to care for, so you can focus on enjoying your trip.
                    Lastly, elevate your casual wardrobe with a stylish tiered skirt made from luxurious polyester net fabric. This knee-length, flared design with a solid color and semi-sheer, gathered surface gives it a trendy, layered look. Perfect for a day out with friends or a relaxed city stroll, this skirt pairs beautifully with funky acrylic earrings, art deco sandals, and square sunglasses with thick frames. It's a chic ensemble that will make you feel like a true Parisian fashionista.
                    With these outfits, you'll be ready to capture the essence of Paris in every photo! Enjoy your trip and make sure to take lots of cute pictures!  '''
                    }]
            )
        else:
            response = client.chat.completions.create(
                model=deployment_name,
                temperature=0.4,
                max_tokens=4096,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},    
                ]
            )
            
        return response

    except Exception as ex:
        print(ex)
        return {"error": str(ex)}

@app.route('/generate_response', methods=['POST'])
def generate_response_endpoint():
    data = request.json
    response_json = data.get('response_json')
    prompt = data.get('prompt')
    print("generate_response is running")
    response = response_generation(response_json, prompt)
    
    return jsonify(response)

@app.route('/identify_intent', methods=['POST'])
def identify_intent_endpoint():
    data = request.json
    user_text = data.get('user_text')
    img_url = data.get('img_url')
    prompts_json = data.get('prompts_json')
    intents_json = data.get('intents_json')

    print("/identify_intent is running")
    print("Received data:")
    print(f"User Text: {user_text}")
    print(f"Image URL: {img_url}")
    print(f"Previous Prompts: {prompts_json}")
    print(f"Previous Intents: {intents_json}")

    if not user_text:
        return jsonify({'error': 'user_text is required'}), 400

    intent = identify_intent(user_text, img_url, prompts_json, intents_json)
    return intent

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

    
    #return response.choices[0].message.content
