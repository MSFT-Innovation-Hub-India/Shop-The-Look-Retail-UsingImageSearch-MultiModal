'use client'
import Image from "next/image";
import styles from './style.module.css';
import useSWR from 'swr';
import axios from 'axios';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function Speech() {
    const router = useRouter();
    const fetcher = (url: string) => axios.get(url).then((res) => res.data);
    const { data, error } = useSWR('http://127.0.0.1:5328/api/listen', fetcher, {
        revalidateOnFocus: false,
        revalidateOnReconnect: false,
        revalidateIfStale: false,
    });

    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (data) {
            setLoading(true);
            setTimeout(() => {
                axios.post('http://127.0.0.1:5328/api/search', { text_query: data })
                    .then(response => {
                        console.log(response);
                        router.push(`/img?data=${encodeURIComponent(JSON.stringify(response.data))}`);
                        setLoading(false);
                    })
                    .catch(error => {
                        console.log(error);
                        setLoading(false);
                    });
            }, 2000);
        }
    }, [data, router]);

    if (loading) {
        return (
            <main className="flex min-h-screen flex-col items-center justify-between p-24">
                <div className="image-animation-container">
                    <Image src="/9.png" alt="Image 1" layout="fill" className="image-animation image1" />
                    <Image src="/10.png" alt="Image 2" layout="fill" className="image-animation image2" />
                </div>
                <div className="loading-text">
                <p className="text-xl font-bold text-center">Ava is fetching the items...</p>
            </div>
            </main>
        );
    }
    

    return (
        <div className={styles.imageContainer}>
            <Image src="/listening.png" layout="fill" alt="image3" />
        </div>
    );
}
