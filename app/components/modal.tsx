'use client'

import React from 'react';
import Image from 'next/image';

interface ModalProps {
  isOpen: boolean;
  imageURL: string;
  imageName: string;
  onClose: () => void;
}

const Modal: React.FC<ModalProps> = ({ isOpen, imageURL, imageName, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-75 z-50">
      <div className="bg-white p-4 rounded shadow-lg max-w-lg mx-4 relative">
        <button
          onClick={onClose}
          className="absolute top-2 right-2 text-gray-500 hover:text-gray-700"
        >
          &times;
        </button>
        <Image src={imageURL} alt={imageName} layout="responsive" width={500} height={500} />
        <h2 className="text-xl mt-4">{imageName}</h2>
      </div>
    </div>
  );
};

export default Modal;
