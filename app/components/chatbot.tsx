'use client'

import React, { useState, useRef } from 'react';
import { IoMicOutline, IoImagesOutline, IoSend, IoClose } from 'react-icons/io5';
import axios from 'axios';
import { useHeader } from './Header';

const Chatbot = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<string[]>([]);
  const { setIsShrunk } = useHeader();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [imageDimensions, setImageDimensions] = useState<{ width: number; height: number } | null>(null);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input) return;

    const response = await axios.post('/api/echo', { message: input });
    setMessages([...messages, `User: ${input}`, `Bot: ${response.data.message}`]);
    setInput('');
    setIsShrunk(true);
  };

  const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // Upload the file to the server
      const formData = new FormData();
      formData.append('file', file);
  
      try {
        const response = await axios.post('https://search.gentleplant-806536f4.swedencentral.azurecontainerapps.io/upload_image', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
  
        const { image_url, filename } = response.data;
        console.log('File uploaded, image URL:', image_url);

        // Create an Image object to get its natural dimensions
        const img = new Image();
        img.src = image_url;
        img.onload = () => {
          setImageDimensions({ width: img.width, height: img.height });
        };

        setImagePreview(image_url);
      } catch (error) {
        console.error('Error uploading file:', error);
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
    setImageDimensions(null);
  };

  return (
    <div className="flex items-center justify-center h-screen bg-white">
      <div className="w-full flex flex-col items-center">
        <div className="justify-center pt-1 max-w-7xl w-full max-h-[70vh] h-auto flex-grow bg-white p-4 rounded-lg border-2 border-zinc-200 overflow-y-auto">
          {messages.map((msg, index) => (
            <p key={index} className={`mb-2 ${msg.startsWith('User') ? 'text-black' : 'text-black'}`}>
              {msg}
            </p>
          ))}
        </div>
        <form onSubmit={sendMessage} className='fixed bottom-4 mx-auto bg-black w-[70%] p-0 rounded-3xl'>
        {imagePreview && (
          <div
            className="relative p-3 pr-3"
            style={{
              width: '48px', // Slightly larger than icons
              height: '48px', // Same height to maintain aspect ratio
            }}
          >
            <img
              src={imagePreview}
              alt="Preview"
              className="absolute w-full h-full object-cover" // Adjust to fit within container
              style={{ transform: 'scale(0.7)' }} // Scale down the image
            />
            <button
              type="button"
              onClick={handleImageClose}
              className="absolute pr-1.5 p-1 bg-red-500 rounded-full"
            >
              <IoClose color='white' size={12} />
            </button>
          </div>
        )}
          <div className="flex items-center justify-center py-2 space-x-2">
            <button type="button" className='p-2 bg-transparent'>
              <IoMicOutline color='white' size={30} />
            </button>
            <button type="button" className='p-2 bg-transparent' onClick={handleImageButtonClick}>
              <IoImagesOutline color='white' size={30} />
            </button>
            <input
              type="search"
              placeholder='How can I help'
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className='w-[85%] p-4 rounded-3xl bg-black text-white focus:outline-none'
            />
            <div className="flex space-x-2">
              <button type="submit" className='p-2 bg-transparent'>
                <IoSend color='white' size={30} />
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