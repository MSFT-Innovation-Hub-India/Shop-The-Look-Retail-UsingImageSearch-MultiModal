
# Shop the Look

A Multi modal Generative AI powered solution that implements Shop the Look capabilities for Retail users

## Function Features
- Users can upload an image and search for matching apparal
- Users can upload an image, point to a particular item in the image using natural language and search for matching items. This involves the gpt-4o multi modal capabilities to describe the item being pointed to, create an enriched search prompt and use Azure AI Search to return matching items from the Catalog
- Showcase how catalog enrichment can be done on the fly, by using gpt-4o model to generate a compelling description of each item in the catalog search results, based on the image of the items


## Features

- Light/dark mode toggle
- Live previews
- Fullscreen mode
- Cross platform


## Tech Stack

**Client:** Streamlit

**Server:** Flask

**Azure Services:** Azure AI Search, Azure OpenAI, Azure AI Vision

**Deployment:** Azure App Service


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`AZURE_OPENAI_ENDPOINT`

`AZURE_OPENAI_API_KEY`

`AZURE_OAI_DEPLOYMENT`

`AZURE_COMPUTER_VISION_ENDPOINT`

`AZURE_COMPUTER_VISION_KEY`

`BLOB_CONNECTION_STRING`

`BLOB_CONTAINER_NAME`

`AZURE_SEARCH_ADMIN_KEY`

`AZURE_SEARCH_SERVICE_ENDPOINT`

`BLOB_CONNECTION_STRING`

`BLOB_CONTAINER_NAME_IMG`




## Authors

- [@goy4l](https://www.github.com/goy4l)
- [@ashwinchandra08](https://www.github.com/ashwinchandra08)
- [@tanishqatp](https://www.github.com/tanishqatp)
- [@YohanTheNohan](https://www.github.com/YohanTheNohan)
- [@AutisticCoder-9000](https://github.com/AutisticCoder-9000)
