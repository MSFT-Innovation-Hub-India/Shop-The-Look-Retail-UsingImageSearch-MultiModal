import openai
import os
import json
import time
import requests
from dotenv import load_dotenv
from pathlib import Path
from openai import AzureOpenAI
from typing import Optional
#from intent_identification import *
from flask import Flask, request, jsonify
from requests.models import Response
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv(".env")

# Azure OpenAI setup
openai.api_type = "azure"
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_ENDPOINT = os.getenv("AZURE_OPENAI_API_ENDPOINT")
#AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version="2024-05-01-preview",
    azure_endpoint=AZURE_OPENAI_API_ENDPOINT
)

def send_request_to_search_endpoint(assistant_response, img_url):
    if assistant_response == "This is a follow up":
        return {"status": "Follow up detected"}
    else:
        text_query = assistant_response  # Assuming this is the vector search query
        response = requests.post('http://localhost:8080/search', json={"text_query": text_query, "image_url": img_url})
        #result = response.json()
        return response.json()
        #return {"status": "Request processed successfully", "result": result}
    
def analyze_image(img_url):
    # Make an API call to OpenAI to analyze the image
    # Prepare the prompt with the image URL
    response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                { "role": "system", "content": "You are an expert in fashion design. Describe what the person or people in the image are wearing. Including their accessories.\
                    Also identify their gender."
                },

                { "role": "user", "content": [  
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
    
    return response.choices[0].message.content

# Define the identify_intent function
def intent(user_text, img_url):
    # Your implementation for intent identification
    
    return 

# Function to poll the run until completion
def poll_run_till_completion(
    client: AzureOpenAI,
    thread_id: str,
    run_id: str,
    available_functions: dict,
    verbose: bool,
    max_steps: int = 10,
    wait: int = 3,
) -> None:
    if (client is None and thread_id is None) or run_id is None:
        print("Client, Thread ID and Run ID are required.")
        return
    try:
        cnt = 0
        while cnt < max_steps:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if verbose:
                print("Poll {}: {}".format(cnt, run.status))
            cnt += 1
            if run.status == "requires_action":
                tool_responses = []
                if (
                    run.required_action.type == "submit_tool_outputs"
                    and run.required_action.submit_tool_outputs.tool_calls is not None
                ):
                    tool_calls = run.required_action.submit_tool_outputs.tool_calls

                    for call in tool_calls:
                        if call.type == "function":
                            if call.function.name not in available_functions:
                                raise Exception("Function requested by the model does not exist")
                            function_to_call = available_functions[call.function.name]
                            tool_response = function_to_call(**json.loads(call.function.arguments))
                            tool_responses.append({"tool_call_id": call.id, "output": tool_response})

                run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread_id, run_id=run.id, tool_outputs=tool_responses
                )
            if run.status == "failed":
                print("Run failed.")
                break
            if run.status == "completed":
                break
            time.sleep(wait)
    except Exception as e:
        print(e)

# Function to create a message
def create_message(
    client: AzureOpenAI,
    thread_id: str,
    role: str = "",
    content: str = "",
    file_ids: Optional[list] = None,
    metadata: Optional[dict] = None,
    message_id: Optional[str] = None,
) -> any:
    if metadata is None:
        metadata = {}
    if file_ids is None:
        file_ids = []

    if client is None:
        print("Client parameter is required.")
        return None

    if thread_id is None:
        print("Thread ID is required.")
        return None

    try:
        if message_id is not None:
            return client.beta.threads.messages.retrieve(thread_id=thread_id, message_id=message_id)

        if file_ids is not None and len(file_ids) > 0 and metadata is not None and len(metadata) > 0:
            return client.beta.threads.messages.create(
                thread_id=thread_id, role=role, content=content, file_ids=file_ids, metadata=metadata
            )

        if file_ids is not None and len(file_ids) > 0:
            return client.beta.threads.messages.create(
                thread_id=thread_id, role=role, content=content, file_ids=file_ids
            )

        if metadata is not None and len(metadata) > 0:
            return client.beta.threads.messages.create(
                thread_id=thread_id, role=role, content=content, metadata=metadata
            )

        return client.beta.threads.messages.create(thread_id=thread_id, role=role, content=content)

    except Exception as e:
        print(e)
        return None

# Function to retrieve and print messages
def retrieve_and_print_messages(
    client: AzureOpenAI, thread_id: str, verbose: bool, out_dir: Optional[str] = None
) -> any:
    if client is None and thread_id is None:
        print("Client and Thread ID are required.")
        return None
    try:
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        with open('messages.json', 'w') as file:
            file.write(messages.model_dump_json(indent=2))
        data = json.loads(messages.model_dump_json(indent=2))
        assistant_response = data['data'][0]['content'][0]['text']['value']
        display_role = {"user": "User query", "assistant": "Assistant response"}

        prev_role = None

        if verbose:
            print("\n\nCONVERSATION:")
        for md in reversed(messages.data):
            if prev_role == "assistant" and md.role == "user" and verbose:
                print("------ \n")

            for mc in md.content:
                if mc.type == "text":
                    txt_val = mc.text.value
                elif mc.type == "image_file":
                    image_data = client.files.content(mc.image_file.file_id)
                    if out_dir is not None:
                        out_dir_path = Path(out_dir)
                        if out_dir_path.exists():
                            image_path = out_dir_path / (mc.image_file.file_id + ".png")
                            with image_path.open("wb") as f:
                                f.write(image_data.read())

                if verbose:
                    if prev_role == md.role:
                        print(txt_val)
                    else:
                        print("{}:\n{}".format(display_role[md.role], txt_val))
            prev_role = md.role
        return assistant_response,messages
    except Exception as e:
        print(e)
        return None

@app.route('/create-thread', methods=['POST'])
def create_thread():
    thread = client.beta.threads.create()
    return jsonify({"thread_id": thread.id})

@app.route('/process-request', methods=['POST'])
def process_request():
    data = request.json
    user_text = data.get('user_text')
    img_url = data.get('img_url')
    thread_id = data.get('thread_id')
    assistant_id = data.get('assistant_id')

    if img_url is not None:
        # Analyze the image
        image_description = analyze_image(img_url)
    
        # Create a thread
        #thread = client.beta.threads.create()

        # Combine user text and image description
        combined_input = f"User Query: {user_text}\nImage Description: {image_description}"
        
        # Create a message
        create_message(client, thread_id, role="user", content=combined_input)
    else:
        # Create a message
        create_message(client, thread_id, role="user", content=user_text)

    # Prompt the model to identify intent
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id

    )

    # Poll until completion
    poll_run_till_completion(
        client=client, thread_id=thread_id, run_id=run.id, available_functions={"intent": intent}, verbose=True
    )

    # Retrieve and print messages
    assistant_response, messages = retrieve_and_print_messages(client=client, thread_id=thread_id, verbose=True)
    print("Assistant Response from function", assistant_response)
    
    if assistant_response == "This is a follow-up":
        create_message(client, thread_id, role="user", content=user_text)
        run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=os.getenv("AZURE_ASSISTANT_RESPONSE") #Response_Generation assistant 
        )

            # Poll until completion
        poll_run_till_completion(
            client=client, thread_id=thread_id, run_id=run.id, available_functions={"intent": intent}, verbose=True
        )
        
        followUp_response, messages = retrieve_and_print_messages(client=client, thread_id=thread_id, verbose=True)
                
            # Create the dictionary
        response_dict = {
            "assistant_id": os.getenv("AZURE_ASSISTANT_RESPONSE"),
            "value": followUp_response
        }

        # Convert the dictionary to a JSON string
        response_json = json.dumps(response_dict)

        # Print or use the JSON string as needed
        print(response_json)

        return followUp_response

    else:
        # Call the new function to handle the assistant response
        search_response = send_request_to_search_endpoint(assistant_response, img_url)
        formatted_response = ""
        for item in search_response:
            formatted_response += (
                f"Name: {item['name']}\n"
                f"Price: {item['price']}\n"
                f"Score: {item['score']}\n"
                f"URL: {item['url']}\n\n"
            )
        #Format the json result into a string so it can be stored in a thread
        formatted_search_response = formatted_response.strip()

        print("Formatted Search Response", formatted_search_response)

        # Create a message with the search results
        create_message(client,thread_id, role="user", content=assistant_response)
        create_message(client, thread_id, role="assistant", content=formatted_search_response)
        
        return jsonify(search_response)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5328)

'''
# Updated available functions dictionary
available_functions = {"intent": intent}
verbose_output = True

# Declare the Assistant's ID
assistant_id = "asst_18DYPu0YR2FIntqzm8NQhZ7k"

# Fetch the assistant
assistant = client.beta.assistants.retrieve(
    assistant_id=assistant_id
)

# Create a thread
thread = client.beta.threads.create()

# User input text and image URL
user_text = "I want to find a similar jacket"
img_url = "https://images.pexels.com/photos/1536619/pexels-photo-1536619.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"

image_description = analyze_image(img_url)
print(image_description)
# Combine user text and image description
combined_input = f"User Query: {user_text}\nImage Description: {image_description}"

create_message( client=client, thread_id=thread.id, role="user", content=combined_input)

# Prompt the model to identify intent
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

poll_run_till_completion(
    client=client, thread_id=thread.id, run_id=run.id, available_functions=available_functions, verbose=verbose_output
)

# Retrieve and print messages
messages = retrieve_and_print_messages(client=client, thread_id=thread.id, verbose=verbose_output)
'''