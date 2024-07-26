import os
from dotenv import load_dotenv
import json

# Add Azure OpenAI package
from openai import AzureOpenAI

def read_return_policy(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def response_generation(prompt, current_time, order_data, previous_prompts, previous_responses):
    
    file = read_return_policy('returnpolicy.txt') 
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

        system_message = """You are a virtual customer support assistant for retail website Ajio. You must provide users with details about your return policy according to the 
        document that you receive. Provide short and concise responses to user queries. 
        You also receive the current date and time, and the user's order data. If the user asks about their order, use this information to
        decide whether the item that the user is trying to return is eligible for a return.
        Your response should be one or two sentences MAXIMUM. Do not ask the user if they need more assistance. 
        If the question is not about a particular order, find the appropriate information from the policy and return this. Do not add details about their order.
        If the question is about a particular order, use the order data to determine if the item is eligible for a return or answer whatever their question is.
        Only provide information that is relevant to the user's query. Do not provide any additional information.
        """
        
        
        response = client.chat.completions.create(
            model=azure_oai_deployment,
            temperature=0.4,
            max_tokens=4096,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},    
                {"role": "user", "content": file},
                {"role": "user", "content": current_time},
                {"role": "user", "content": order_data},
                # {"role": "user", "content": previous_prompts},
                # {"role": "assistant", "content": previous_responses}
                {"role": "assistant", "content": 'To return an item, log in to your account, go to the "My Account" section, select the order you want to return, and follow the instructions to obtain a Return ID. Your order is eligible for return within 10 days from the delivery date.'},
                {"role": "assistant", "content": "You are eligible to return the jeans you bought on July 10th, as it falls within the 10-day return period for apparel."}
            ]
        )
            
        return response.choices[0].message.content
    
    
    except Exception as ex:
        print(ex)