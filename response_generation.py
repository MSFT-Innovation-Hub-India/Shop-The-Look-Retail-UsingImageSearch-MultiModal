import os
from dotenv import load_dotenv
import json

# Add Azure OpenAI package
from openai import AzureOpenAI

def response_generation(response_json, prompt): 
    try: 
        # Get configuration settings 
        load_dotenv()
        azure_oai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        azure_oai_key = os.getenv("AZURE_OPENAI_KEY")
        azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")
        
        # Initialize the Azure OpenAI client...
        client = AzureOpenAI(
         azure_endpoint = azure_oai_endpoint, 
         api_key=azure_oai_key,  
         api_version="2024-02-15-preview"
         )
        # Create a system message
        # system_message = """
        #     I am a helpful AI assistant designed to enhance your experience by providing what the user wants in an refined and elaborate way.
        #     With the JSON data as context, I aim to deliver comprehensive and detailed responses tailored to your specific queries.
        # """
        # system_message = f"""
        #     I am a helpful AI assistant designed to enhance your experience by providing refined and elaborate responses based on user input and the provided JSON context.
        #     With the given JSON data, I will tailor my responses to your specific queries to deliver comprehensive and detailed information.
        #     """

        system_message = """You are a fashion assistant which provides the user an enticing fashion suggestion,
        based on their request and the description of the suggested clothing item. You are given the user prompt as context. \
        You must use the user prompt only to make the result conversational. The remainder of the response must be based on the description of the suggested clothing item. \
        Assume this description data is the fashion suggestion, so you do not have to suggest new clothing items. \
        If there are multiple items, describe each one in a separate paragraph.
        You may provide only relevant attributes from the description data and answer the users request in a conversational manner.
        Do not give bullet points unless specifically asked. Provide a conversational and enticing paragraph description"""
        
        while True:
            # Read the response from the JSON file

            # Get input text
            # input_text = input("Enter the prompt (or type 'quit' to exit): ")
            # if input_text.lower() == "quit":
            #     break
            # if len(input_text) == 0:
            #     print("Please enter a prompt.")
            #     continue

            # print("\nSending request for summary to Azure OpenAI endpoint...\n\n")
            
             # Add code to send request...
            # Send request to Azure OpenAI model
            if response_json is not None:
                response = client.chat.completions.create(
                    model=azure_oai_deployment,
                    temperature=0.4,
                    max_tokens=4096,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": prompt},
                        # {"role": "user", "content": response_json},
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
                    model=azure_oai_deployment,
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
