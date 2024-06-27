
import os
from openai import AzureOpenAI
import dotenv

dotenv.load_dotenv()

api_base = os.getenv("api_base")
deployment_name = os.getenv("deployment_name")
api_key = os.getenv("api_key")
api_version = os.getenv("api_version")



def gen_caption(img_url, attributes):

    client = AzureOpenAI(
        api_key = api_key,
        api_version = api_version,
        base_url = f"{api_base}/openai/deployments/{deployment_name}",
    )

    

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            { "role": "system", "content": "You are an expert in fashion design.\
              Generate an enticing description for the products in the image\
              make use of the attributes to describe the products. \
              The description that you generate must be such that it \
             can be easily used in a vectory search algorithm" },

            { "role": "user", "content": [  
                { 
                    "type": "text", 
                    "text": "Describe this picture" + attributes
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


def main():
    response = gen_caption("http://assets.myntassets.com/assets/images/17048614/2022/2/4/b0eb9426-adf2-4802-a6b3-5dbacbc5f2511643971561167KhushalKWomenBlackEthnicMotifsAngrakhaBeadsandStonesKurtawit7.jpg")
    print(response)



if __name__ == "__main__":
    main()