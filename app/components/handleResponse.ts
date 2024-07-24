export interface Product {
    name: string;
    price: number;
    score: number;
    url: string;
  }
  
  export interface FormattedMessage {
    text: string;
    imageURL: string;
    price: number;
  }
  
  export function handleFormattedResponse(data: Product[]): FormattedMessage[] {
    return data.map(product => ({
      text: product.name,
      imageURL: product.url,
      price: product.price,
    }));
  }
  