'use client'
import Image from "next/image";
import Link from 'next/link'
import styles from './style.module.css'
import useSWR from 'swr';
import axios from 'axios';
import {useRouter} from 'next/navigation';
import { useEffect } from 'react';
import { Router } from "next/router";

export default function Speech() {

    const fetcher = (url: string) => axios.get(url).then((res) => res.data);
    const {data, error} = useSWR('http://127.0.0.1:5328/api/listen', fetcher, {
        revalidateOnFocus: false, 
        revalidateOnReconnect: false,
        revalidateIfStale: false,
    });

    const router = useRouter();

    useEffect(() => {
        axios.post('http://127.0.0.1:5328/api/search', {
            text_query: data
        }).then(function(response){
            console.log(response);
            // Now that we have the response, we can navigate.
            router.push(`/img?data=${encodeURIComponent(JSON.stringify(response.data))}`);
        }).catch(function(error){
            console.log(error);
        });
    }, [data, router]); // Added dependencies to useEffect.


    return (
        <div className={styles.imageContainer}>
            <Image src="/listening.png" layout="fill" alt="image3" />
        </div>
    )


}