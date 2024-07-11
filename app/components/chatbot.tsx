'use client'

import React, { useState } from 'react';
import { FaMicrophone } from 'react-icons/fa';
import { IoSend } from 'react-icons/io5';
import { MdAddPhotoAlternate } from 'react-icons/md';
import axios from 'axios';

const Chatbot = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<string[]>([]);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input) return;

    const response = await axios.post('/api/echo', { message: input });
    setMessages([...messages, `You: ${input}`, `Bot: ${response.data.message}`]);
    setInput('');
  };

  return (
    <div className="">
      <div className="max-w-6xl mx-auto mt-10 flex flex-col h-screen flex-grow mb-6 bg-gray-100 p-4 rounded-lg shadow-md overflow-y-auto">
        {messages.map((msg, index) => (
          <p key={index} className={`mb-2 ${msg.startsWith('You') ? 'text-blue-500' : 'text-green-500'}`}>
            {msg}
          </p>
        ))}
      </div>
      <form onSubmit={sendMessage} className='fixed bottom-0 w-full mx-auto'>
        <div className="flex items-center justify-center py-2">
          <input
            type="search"
            placeholder='How can I help'
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className='w-[80%] p-4 rounded-3xl bg-slate-800 text-white focus:outline-none'
          />
          <button type="button" className='p-4 bg-transparent'>
            <FaMicrophone color='#1E293B' size={30} />
          </button>
          <button type="submit" className='p-4 bg-transparent'>
            <IoSend color='white' size={30} />
          </button>
          <button type="button" className='p-4 bg-transparent'>
            <MdAddPhotoAlternate color='#1E293B' size={37} />
          </button>
        </div>
      </form>
    </div>
  );
};

export default Chatbot;
