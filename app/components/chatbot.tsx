'use client'

import React, { useState, useRef, useEffect } from 'react';
import { IoMicOutline, IoImagesOutline, IoSend, IoClose } from 'react-icons/io5';
import axios from 'axios';
import { useHeader } from './Header';
import Image from 'next/image';
import userImage from '/public/user.png';
import botImage from '/public/bot.png';
import useThread from '../hooks/useThread';
import { Product, handleFormattedResponse } from './handleResponse';

interface Message {
  type: 'user' | 'bot';
  text: string;
  imageURL?: string;
  price?: number;
}

const Chatbot = () => {
  const [input, setInput] = useState<string>('');
  const [messages, setMessages] = useState<Message[]>([]);
  const { setIsShrunk } = useHeader();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [imageURL, setImageURL] = useState<string>('');

  const chatContainerRef = useRef<HTMLDivElement>(null);
  const latestMessageRef = useRef<HTMLDivElement>(null);

  const threadId = useThread();
  console.log('Thread ID:', threadId);

  const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const localImageUrl = URL.createObjectURL(file);
      setImagePreview(localImageUrl);

      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await axios.post(
          'https://search.gentleplant-806536f4.swedencentral.azurecontainerapps.io/upload_image',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          }
        );

        const { image_url } = response.data;
        setImageURL(image_url);
        console.log('File uploaded, image URL:', image_url);

      } catch (error) {
        console.error('Error uploading file:', error);
      }
    }
  };

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input) return;

    setIsShrunk(true);
    setInput('');
    setImagePreview(null);
    setImageURL('');

    setMessages((prevMessages) => [
      ...prevMessages,
      { type: 'user', text: input, imageURL: imageURL },
    ]);

    if (threadId) {
      const params = {
        user_text: input,
        img_url: imageURL || null,
        thread_id: threadId,
        assistant_id: process.env.NEXT_PUBLIC_AZURE_ASSISTANT_INTENT
      };

      try {
        const processResponse = await axios.post('http://localhost:5328/process-request', params);
        console.log("Process response: ", processResponse.data);

        const isArray = Array.isArray(processResponse.data);
        const hasExpectedFormat = isArray && processResponse.data.every((item: Product) =>
          typeof item === 'object' &&
          'name' in item &&
          'price' in item &&
          'score' in item &&
          'url' in item
        );

        if (hasExpectedFormat) {
          console.log("Response is in the format of response1.");
          const formattedData = handleFormattedResponse(processResponse.data);
            const combinedResponse = formattedData.map(item => ({
            type: 'bot',
            text: item.text,
            imageURL: item.imageURL,
            price: item.price
            }));

            // Store all data in a single message object
            setMessages((prevMessages) => [
            ...prevMessages,
            {
              type: 'bot',
              text: combinedResponse.map(item => item.text).join('\n'),
              imageURL: combinedResponse.map(item => item.imageURL).join('\n'),
              price: parseFloat(combinedResponse.map(item => item.price).join('\n')),
            },
            ]);

            console.log('Messages Added:', combinedResponse);
        } else {
          console.log("Response is not in the format of response1.");
        }
      } catch (error) {
        console.error('Error sending message:', error);
      }
    }
  };

  const handleImageButtonClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleImageClose = () => {
    setImagePreview(null);
  };

  useEffect(() => {
    if (latestMessageRef.current) {
      latestMessageRef.current.scrollIntoView({ behavior: 'smooth', block: 'end' });
    }
  }, [messages]);

  return (
    <div className="flex items-center justify-center h-screen bg-white">
      <div className="w-full flex flex-col items-center">
        <div
          ref={chatContainerRef}
          className="justify-center pt-1 max-w-5xl w-full max-h-[70vh] h-auto flex-grow bg-white p-4 rounded-lg overflow-y-auto"
        >
          {messages.map((msg, index) => (
            <div
              key={index}
              ref={index === messages.length - 1 ? latestMessageRef : null}
              className={`mb-2 flex items-center ${
                msg.type === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {msg.type === 'bot' && (
                <Image
                  src={botImage}
                  alt="Bot"
                  width={48}
                  height={48}
                  className="mr-2 rounded-full"
                />
              )}
              <p
                className={`p-2 rounded-md ${
                  msg.type === 'user' ? 'bg-zinc-100' : 'bg-transparent'
                }`}
              >
                {msg.text}
                {msg.imageURL && <Image src={msg.imageURL} alt="Uploaded" width={50} height={50} />}
              </p>
              {msg.type === 'user' && (
                <Image
                  src={userImage}
                  alt="User"
                  width={48}
                  height={48}
                  className="ml-2 rounded-full"
                />
              )}
            </div>
          ))}
        </div>
        <form
          onSubmit={sendMessage}
          className="fixed bottom-4 mx-auto bg-black w-[70%] p-0 rounded-3xl"
        >
          {imagePreview && (
            <div className="relative ml-8 mr-10 mt-2 mb-0">
              <div
                className="relative w-[50px] h-[50px] overflow-hidden"
                style={{ borderRadius: '8px' }}
              >
                <Image
                  src={imagePreview}
                  alt="Preview"
                  layout="fill"
                  objectFit="cover" 
                />
              </div>
              <button
                type="button"
                onClick={handleImageClose}
                className="absolute bottom-8 left-9 bg-header rounded-full p-1"
              >
                <IoClose color="white" size={12} />
              </button>
            </div>
          )}
          <div className="flex items-center justify-center py-2 space-x-2">
            <button type="button" className="p-2 bg-transparent">
              <IoMicOutline color="white" size={30} />
            </button>
            <button
              type="button"
              className="p-2 bg-transparent"
              onClick={handleImageButtonClick}
            >
              <IoImagesOutline color="white" size={30} />
            </button>
            <input
              type="search"
              placeholder="How can I help"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="w-[85%] p-4 rounded-3xl bg-black text-white focus:outline-none"
            />
            <div className="flex space-x-2">
              <button type="submit" className="p-2 bg-transparent">
                <IoSend color="white" size={30} />
              </button>
            </div>
          </div>
        </form>
        <input
          type="file"
          ref={fileInputRef}
          style={{ display: 'none' }}
          onChange={handleFileSelect}
        />
      </div>
    </div>
  );
};

export default Chatbot;
