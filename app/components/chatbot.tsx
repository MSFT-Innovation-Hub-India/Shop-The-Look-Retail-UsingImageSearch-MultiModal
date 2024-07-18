'use client'

import React, { useState } from 'react';
import { IoMicOutline, IoImagesOutline, IoSend } from 'react-icons/io5';
import axios from 'axios';
import { useHeader } from './Header';

const Chatbot = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<string[]>([]);
  const { setIsShrunk } = useHeader();

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input) return;

    const response = await axios.post('/api/echo', { message: input });
    setMessages([...messages, `You: ${input}`, `Bot: ${response.data.message}`]);
    setInput('');
    setIsShrunk(true);
  };

  return (
    <div className="flex items-center justify-center h-screen bg-white">
      <div className="justify-center pt-1 max-w-7xl w-full max-h-[70vh] h-auto flex-grow bg-white p-4 rounded-lg border-2 border-zinc-200 overflow-y-auto">
        {messages.map((msg, index) => (
          <p key={index} className={`mb-2 ${msg.startsWith('You') ? 'text-black' : 'text-black'}`}>
            {msg}
          </p>
        ))}
      </div>
      <form onSubmit={sendMessage} className='fixed bottom-4 mx-auto bg-black w-[70%] p-0  rounded-3xl'>
        <div className="flex items-center justify-center py-2 space-x-2">
        <button type="button" className='p-2 bg-transparent'>
              <IoMicOutline color='white' size={30} />
            </button>
            <button type="button" className='p-2 bg-transparent'>
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
    </div>
  );
};

export default Chatbot;
