'use client'

import { Message, Product } from './chatbot';
  
  export function handleFormattedResponse(data: Product[]): Message[] {
    return data.map(product => ({
      type: 'bot',
      text: product.name,
      imageURL: product.url,
      price: product.price
    }));
  }
  