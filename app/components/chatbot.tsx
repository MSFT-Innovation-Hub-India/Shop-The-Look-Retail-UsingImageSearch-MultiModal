'use client'

import React, { useState, useRef, useEffect } from 'react';
import { IoMicOutline, IoImagesOutline, IoSend, IoClose } from 'react-icons/io5';
import { RiShoppingBag4Fill, RiShoppingCart2Line } from "react-icons/ri";
import axios from 'axios';
import { useHeader } from './Header';
import Image from 'next/image';
import userImage from '/public/user.png';
import botImage from '/public/bot.png';
import useThread from '../hooks/useThread';
import { handleFormattedResponse } from './handleResponse';
import styles from './chatbot.module.css';

export interface Message {
  type: 'user' | 'bot';
  text: string;
  image_url: string;
  imageWithPrices?: { imageURL: string; price: number; name: string }[];
}

export interface Product {
  name: string;
  price: number;
  url: string;
}

export interface FollowUp {
  value: string;
}

const Chatbot = () => {
  const [input, setInput] = useState<string>('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState<boolean>(false); // Loading state
  const { setIsShrunk } = useHeader();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [imageURL, setImageURL] = useState<string>('');
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [modalImageURL, setModalImageURL] = useState<string | null>(null);
  const [modalProductDescription, setModalProductDescription] = useState<string>('');

  const [isClicked, setIsClicked] = useState(false);

  const [micButtonColor, setMicButtonColor] = useState<string>(''); // New state for mic button color

  // New state for recognized text
  const [recognizedText, setRecognizedText] = useState<string>('');

  const chatContainerRef = useRef<HTMLDivElement>(null);
  const latestMessageRef = useRef<HTMLDivElement>(null);

  const threadId = useThread();

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
  
    setLoading(true); // Set loading to true
    setIsShrunk(true);
    setInput('');
    setImagePreview(null);
    setImageURL('');
  
    // Send user message
    setMessages(prevMessages => [
      ...prevMessages,
      { type: 'user', text: input, image_url: imageURL }
    ]);
  
    if (threadId) {
      const params = {
        user_text: input || recognizedText,
        img_url: imageURL || null,
        thread_id: threadId,
        assistant_id: process.env.NEXT_PUBLIC_AZURE_ASSISTANT_INTENT
      };
  
      try {
        const processResponse = await axios.post('http://localhost:5328/process-request', params);
        console.log("Process response: ", processResponse.data);

        // Use handleFormattedResponse to transform response data
        const formattedMessage = handleFormattedResponse(processResponse.data);

        // Add the formatted message to messages
        setMessages(prevMessages => [
          ...prevMessages,
          formattedMessage
        ]);

        console.log('Messages Added:', formattedMessage);

      } catch (error) {
        console.error('Error sending message:', error);
      } finally {
        setLoading(false); // Set loading to false
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

  const openModal = (imageURL: string, description: string) => {
    setModalImageURL(imageURL);
    setModalProductDescription(description);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  useEffect(() => {
    if (latestMessageRef.current) {
      latestMessageRef.current.scrollIntoView({ behavior: 'smooth', block: 'end' });
    }
  }, [messages]);

  const renderText = (text: string) => {
    // Replace Markdown-style bold syntax with HTML <strong> tags
    const formattedText = text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Handle bold text
      .replace(/\n/g, '<br>'); // Replace newlines with <br> tags
    return { __html: formattedText };
  };

  // Function to handle the mic button click
  // Function to handle the mic button click
const handleMicMouseDown = async () => {
  setIsClicked(true);
  setMicButtonColor('red'); // Set mic button color to red
  try {
    const response = await axios.post('http://localhost:5000/listen'); 
    if (response.status === 200) {
      const { recognized_text } = response.data;
      console.log('Recognized Text:', recognized_text);
      setRecognizedText(recognized_text);

      // Update input state with recognized text
      setInput(recognized_text);

    } else {
      console.error('Error recognizing speech:', response.statusText);
    }
  } catch (error) {
    console.error('Error fetching from backend:', error);
  } finally {
    setIsClicked(false);
  }
};

const handleMicMouseUp = async () => {
    setIsClicked(false);
    setMicButtonColor(''); // Reset mic button color
  };

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
              <div
                className={`p-2 rounded-md ${
                  msg.type === 'user' ? 'bg-zinc-100' : 'bg-transparent'
                }`}
              >
                {msg.type === 'bot' ? (
                  <p dangerouslySetInnerHTML={renderText(msg.text)}></p>
                ) : (
                  <p>{msg.text}</p>
                )}
                {msg.image_url && <Image src={msg.image_url} alt='uploaded' width={75} height={75} className='justify-center'></Image>}
                {msg.imageWithPrices && (
                  <div className="flex space-x-2 overflow-x-auto">
                    {msg.imageWithPrices.map((imageWithPrice, idx) => (
                      <div
                        key={idx}
                        className="flex flex-col items-center border border-gray-300 rounded cursor-pointer"
                        onClick={() => openModal(imageWithPrice.imageURL, imageWithPrice.name)}
                      >
                        <Image
                          src={imageWithPrice.imageURL}
                          alt="Product"
                          width={300}
                          height={300}
                          className="border border-gray-300 rounded"
                          objectFit='cover'
                        />
                        <p>₹{Math.floor(imageWithPrice.price)}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
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
          {loading && (
            <div className="flex justify-center items-center py-4">
              <p className="text-gray-500 mr-2">Getting your response...</p>
              <div className={styles.spinner}></div>
            </div>
          )}
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
          <button
            type="button"
            onMouseDown={handleMicMouseDown}
            onMouseUp={handleMicMouseUp}
            className={`text-2xl text-white p-2 rounded-full mx-2 ${micButtonColor ? 'bg-red-500' : ''}`} // Apply red color when pressed
          >
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
      {isModalOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <div className="relative bg-white rounded-lg w-[80%] max-w-4xl p-4 flex">
            <button
              onClick={closeModal}
              className="absolute top-2 right-2 text-gray-600"
            >
              <IoClose size={24} />
            </button>
            {modalImageURL && (
              <div className="flex-shrink-0 w-1/2 pr-4">
                <Image
                  src={modalImageURL}
                  alt="Modal Image"
                  width={600}
                  height={600}
                  className="w-full h-auto rounded"
                  objectFit='cover'
                />
              </div>
            )}
            {modalProductDescription && (
              <div className="flex-1">
                <p className="text-lg pt-9 mb-4">{modalProductDescription}</p>
                <div className="flex flex-col items-start space-y-2">
                  <button
                    onClick={closeModal}
                    className="bg-header text-white px-4 py-2 rounded-lg hover:bg-black flex items-center"
                  >
                    <RiShoppingCart2Line size={15} className="mr-2" />
                    Add to Cart
                  </button>
                  <button
                    onClick={closeModal}
                    className="bg-header text-white px-4 py-2 rounded-lg hover:bg-black flex items-center"
                  >
                    <RiShoppingBag4Fill size={15} className="mr-2" />
                    Buy now
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Chatbot;
