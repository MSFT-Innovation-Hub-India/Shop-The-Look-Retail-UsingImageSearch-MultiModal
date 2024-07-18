'use client'

import React, { createContext, useState, useContext, ReactNode } from 'react';

interface HeaderContextProps {
  isShrunk: boolean;
  setIsShrunk: (value: boolean) => void;
}

const HeaderContext = createContext<HeaderContextProps | undefined>(undefined);

export const HeaderProvider = ({ children }: { children: ReactNode }) => {
  const [isShrunk, setIsShrunk] = useState(false);

  return (
    <HeaderContext.Provider value={{ isShrunk, setIsShrunk }}>
      {children}
    </HeaderContext.Provider>
  );
};

export const useHeader = () => {
  const context = useContext(HeaderContext);
  if (!context) {
    throw new Error('useHeader must be used within a HeaderProvider');
  }
  return context;
};
