// components/Explore.tsx
import React from 'react';
import { Box, Container, Heading, Link, Text } from '@chakra-ui/react';

const fashionTrends = [
  {
    title: "Dress for Your Next Haldi Inspired by Bollywood Women",
    url: "https://www.femina.in/fashion/trends/dress-for-your-next-haldi-inspired-by-bollywood-women-284593.html",
  },
  {
    title: "Wimbledon Is Full of Menswear Bangers and Here Are the Best",
    url: "https://www.gqindia.com/gallery/wimbledon-is-full-of-menswear-bangers-and-here-are-the-best",
  },
  {
    title: "Here's Who Won Milan Fashion Week",
    url: "https://www.gqindia.com/content/heres-who-won-milan-fashion-week",
  },
  {
    title: "Halter Neck Blouses Are Back: These Bollywood Women Are Proof",
    url: "https://www.femina.in/fashion/trends/halter-neck-blouses-are-back-these-bollywood-women-are-proof-284476.html",
  },
  {
    title: "Swimsuits as Summer Tops",
    url: "https://www.femina.in/fashion/trends/swimsuits-as-summer-tops-284069.html",
  },
  {
    title: "Best Suits for Men: How to Pick Out the Perfect Suit for Every Occasion",
    url: "https://www.gqindia.com/content/best-suits-for-men-how-to-pick-out-the-perfect-suit-that-is-suitable-for-every-occasion",
  },
  {
    title: "Printed Styles to Wear This Summer",
    url: "https://www.femina.in/fashion/trends/printed-styles-to-wear-this-summer-263136.html",
  },
  {
    title: "Here's Why Hidesigns Should Be on Your Radar",
    url: "https://www.femina.in/fashion/trends/heres-why-hidesigns-should-be-on-your-radar-283862.html",
  },
];

const Explore = () => {
  return (
    <Container maxW="container.md" mt={8}>
      <Heading mb={6}>Explore Recent Fashion Trends</Heading>
      {fashionTrends.map((trend, index) => (
        <Box key={index} mb={4}>
          <Link href={trend.url} isExternal color="teal.500">
            <Text fontSize="lg" fontWeight="bold">{trend.title}</Text>
          </Link>
        </Box>
      ))}
    </Container>
  );
};

export default Explore;
