'use client'
import Image from 'next/image';
import {useRouter} from 'next/navigation';
import { useEffect } from 'react';
import useSWR from 'swr';
import axios from 'axios';

const fetcher = (url: string) => axios.get(url).then((res) => res.data);

export default function MyComponent() {

  const {data, error} = useSWR('http://127.0.0.1:5328/api/detect', fetcher, {
    revalidateOnFocus: false, 
    revalidateOnReconnect: false,
    revalidateIfStale: false,
  });
  const apiReturnedTrue = data === "eyes detected";

  const router = useRouter();

  // Handle error state
  // console.log(error)
  // console.log(data)
  // if (error) return <div>Failed to load</div>;
  // Handle loading state
  // if (!data) return <div>Loading...</div>;

  useEffect(() => {
    if (apiReturnedTrue) {
      router.push('/listening');
    }
  }, [apiReturnedTrue, router]);

  // Render the images while waiting for the API to return true
  return (
        <div>
          <main className="flex min-h-screen flex-col items-center justify-between p-24">
            <div className="image-animation-container">
              <Image src="/close.png" alt="Image 1" layout="fill" className="image-animation image1" />
              <Image src="/open.png" alt="Image 2" layout="fill" className="image-animation image2" />
            </div>
          </main>
        </div>
  );
}

