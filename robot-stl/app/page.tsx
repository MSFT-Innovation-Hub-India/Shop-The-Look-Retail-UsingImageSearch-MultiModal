'use client'
import Image from 'next/image';
import Head from 'next/head';
import {useRouter} from 'next/navigation';
import { cache, useEffect, useState } from 'react';
import useSWR, { mutate } from 'swr';
import axios from 'axios';
import { startInactivityDetection } from './inactivity'; // Import your inactivity detector

const fetcher = (url: string) => axios.get(url).then((res) => res.data);

export default function MyComponent() {

  useEffect(() => {
    startInactivityDetection(); // Start inactivity detection
    // Clear sessionStorage when component mounts
    try {
      sessionStorage.clear();
      //mutate(() => true, undefined, { revalidate: false });
    } catch (error) {
      console.error('Failed to clear sessionStorage:', error);
    }
  }, []);
  
  const {data, error} = useSWR('http://127.0.0.1:5328/api/detect', fetcher, {
    revalidateOnFocus: false, 
    revalidateOnReconnect: false,
    revalidateIfStale: false,
    // revalidateOnMount:false,
  });


  const router = useRouter();

  const [apiReturnedTrue, setApiReturnedTrue] = useState(false);
  console.log(data)

  useEffect(() => {
    // console.log(apiReturnedTrue)
    if(data === "eyes detected"){
      setApiReturnedTrue(true);
    }
    console.log(apiReturnedTrue)
  }, [data]);
  // Handle error state
  // console.log(error)
  // console.log(data)
  // if (error) return <div>Failed to load</div>;
  // Handle loading state
  // if (!data) return <div>Loading...</div>;

  useEffect(() => {
    if (apiReturnedTrue) {
      router.push('/listening');
      setApiReturnedTrue(false);
    }
  }, [apiReturnedTrue, router]);

  // Render the images while waiting for the API to return true
  return (
        <div>
          <title>Shop the Look</title>
          <main className="flex min-h-screen flex-col items-center justify-between p-24">
            <div className="image-animation-container">
              <Image src="/close.png" alt="Image 1" layout="fill" className="image-animation image1" />
              <Image src="/open.png" alt="Image 2" layout="fill" className="image-animation image2" />
            </div>
          </main>
        </div>
  );
}

