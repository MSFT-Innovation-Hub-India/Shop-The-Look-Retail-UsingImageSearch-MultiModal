'use client';

import { Message, Product } from './chatbot';

// Function to handle formatting of response data into a Message object
export function handleFormattedResponse(data: Product[] | { assistant_id: string; value: string }): Message {
  // Check if data is an array of Product objects
  if (Array.isArray(data) && data.every((item: Product) => 'name' in item && 'price' in item && 'url' in item)) {
    return {
      type: 'bot',
      text: '', // Optionally include text here if needed
      image_url: '', // Provide a default value for imageURL
      imageWithPrices: data.map(product => ({
        imageURL: product.url,
        price: product.price
      }))
    };
  } 
  // Check if data is an object with assistant_id and value
  else if ('assistant_id' in data && 'value' in data) {
    return {
      type: 'bot',
      text: data.value, // Use the value field for the message text
      image_url: '', // Provide a default value for imageURL
      imageWithPrices: [] // No images or prices in this format
    };
  }
  // Handle unrecognized formats
  else {
    console.log('Unrecognized response format.');
    return {
      type: 'bot',
      text: 'Unrecognized response format.',
      image_url: '', // Provide a default value for imageURL
      imageWithPrices: []
    };
  }
}
