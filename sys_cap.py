import os
from dotenv import load_dotenv
import json

# Add Azure OpenAI package
from openai import AzureOpenAI

def main(): 
    try: 
        # Get configuration settings 
        load_dotenv()
        azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
        azure_oai_key = os.getenv("AZURE_OAI_KEY")
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
        based on their request and the description of the suggested clothing item. 
        You may provide only relevant attributes from the JSON data and answer the users request in a conversational manner."""

        while True:
            # Read the response from the JSON file
            with open("response.json", "r") as f:
                response_content = json.load(f)

            # Get input text
            input_text = input("Enter the prompt (or type 'quit' to exit): ")
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue

            print("\nSending request for summary to Azure OpenAI endpoint...\n\n")
            
             # Add code to send request...
            # Send request to Azure OpenAI model
            response = client.chat.completions.create(
                model=azure_oai_deployment,
                temperature=0.4,
                max_tokens=4096,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": input_text},
                    {"role": "assistant", "content": json.dumps(response_content, indent=2)}     
                ]
            )
            generated_text = response.choices[0].message.content

            # Print the response
            print(generated_text + "\n")
            #print(response.model_dump_json(indent=2))
            

    except Exception as ex:
        print(ex)

if __name__ == '__main__': 
    main()