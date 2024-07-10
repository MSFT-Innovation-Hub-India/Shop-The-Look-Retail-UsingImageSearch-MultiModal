'use client'
import Image from 'next/image';
import {useRouter, useSearchParams} from 'next/navigation';
import { useEffect } from 'react';
import useSWR from 'swr';
import axios from 'axios';

export default function Take(){
    const searchParams = useSearchParams();
    const data = searchParams.get('item');
    let jsonData = {"name": "", "url": ""};
    console.log(data)

    const router = useRouter();
    
    if (data == null) {
        // Safe to use 'data' here
        <div>Loading...</div>
      }
      else{
        jsonData = JSON.parse(data);
      }

    let responseText = false
    
    useEffect(() => {
        axios.post('http://127.0.0.1:5328/api/speak', {
          text: "Sure! Follow me."
        }).then(function(response){
          console.log(response)
          responseText = response.data == "Spoken";
        }).catch(function(error){
          console.log(error)
        })
      }, [data])

      useEffect(() => {
        if (responseText) {
          router.push('/');
        }
      }, [responseText, router]);
    
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