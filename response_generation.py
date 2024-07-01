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

        system_message = """
            You are an intelligent fashion assistant designed to provide users with 
            personalized fashion advice based on their queries and the image results from Azure AI Search. 
            When interacting with the user, incorporate the relevant details from the provided JSON data, 
            including descriptions of the fashion items found in the image results with proper context, to answer their questions in a friendly and engaging manner. 
            Ensure your responses are concise, informative, and tailored to the user's needs, drawing directly from the Azure AI Search image results.
        """
        
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
            response = client.chat.completions.create(
                model=azure_oai_deployment,
                temperature=0.4,
                max_tokens=4096,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": response_json}     
                ]
            )
            
            # print(response)
            generated_text = response.choices[0].message.content

            # Print the response
            # print(generated_text + "\n")
            #print(response.model_dump_json(indent=2))
            
            return response

    except Exception as ex:
        print(ex)
