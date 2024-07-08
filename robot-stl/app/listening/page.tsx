'use client'
import Image from "next/image";
import Link from 'next/link'
import styles from './style.module.css'
import useSWR from 'swr';
import axios from 'axios';

export default function Speech() {

    const fetcher = (url: string) => axios.get(url).then((res) => res.data);
    const {data, error} = useSWR('http://127.0.0.1:5328/api/listen', fetcher, {
        revalidateOnFocus: false, 
        revalidateOnReconnect: false,
        revalidateIfStale: false,
    });

    try {
        const response = axios.post('http://127.0.0.1:5328/api/search', {
          image_url: null,
          text_query : data,
          // add more data if needed
        });
      } catch (error) {
        console.log(error);
      }

    return (
        <div className={styles.imageContainer}>
            <Image src="/listening.png" layout="fill" alt="image3" />
        </div>
    )


}