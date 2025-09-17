import type { Metadata } from 'next';
import './globals.css';
import { ChakraProvider } from '@chakra-ui/react';
import { HeaderProvider } from './components/Header';

export const metadata: Metadata = {
  title: 'Shop the Look',
  description: 'A Multi modal Generative AI powered solution that implements Shop the Look capabilities for Retail users',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body style={{ fontFamily: 'system-ui, -apple-system, sans-serif' }}>
        <ChakraProvider>
          <HeaderProvider>
            {children}
          </HeaderProvider>
        </ChakraProvider>
      </body>
    </html>
  );
}
 
