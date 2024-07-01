import requests
from response_generation import *

def main():
    # Take image URL and text prompt from the user
    image_url = input("Enter the image URL: ")
    prompt = input("Enter the text prompt: ")

    # Send the data to the endpoint
    try:
        params = {'image_url': image_url, 'text_query': prompt}
        response = requests.post("http://localhost:8080/search", json=params)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Print the response from the server
        
        description_response = response.json()
        url_response = description_response[0]['url']
        description_response = description_response[0]['name']
        
        openai_response = response_generation(description_response, prompt)
        print(openai_response.choices[0].message.content)
        print(url_response)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
