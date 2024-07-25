'use client';

import { FollowUp, Message, Product } from './chatbot';

// Type guard to check if data is a Product array
function isProductArray(data: any): data is Product[] {
  return Array.isArray(data) && data.every((item: any) =>
    'name' in item && 'price' in item && 'url' in item
  );
}

// Function to handle formatting of response data into a Message object
export function handleFormattedResponse(data: Product[] | FollowUp): Message {
  console.log('Received data:', data);

  if (!data) {
    console.log('Data is undefined or null.');
    return {
      type: 'bot',
      text: 'Unrecognized response format.',
      image_url: '',
      imageWithPrices: []
    };
  }

  // Check if data is a Product array
  if (isProductArray(data)) {
    console.log('Data is a Product array.');
    return {
      type: 'bot',
      text: '', // Optionally include text here if needed
      image_url: '',
      imageWithPrices: data.map(product => ({
        imageURL: product.url,
        price: product.price
      }))
    };
  } else {
    // Assume data is a FollowUp and extract value
    let followUpValue: string;

    if (typeof data === 'string') {
      try {
        const parsedData: FollowUp = JSON.parse(data);
        followUpValue = parsedData.value;
      } catch (e) {
        console.log('Error parsing data as JSON:', e);
        followUpValue = data;
      }
    } else {
      followUpValue = data.value;
    }

    console.log('FollowUp value:', followUpValue); // Log the value from FollowUp
    return {
      type: 'bot',
      text: followUpValue,
      image_url: '',
      imageWithPrices: []
    };
  }
}