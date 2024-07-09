'use client'
import Image from 'next/image';
import styles from './style.module.css';
import { useSearchParams } from 'next/navigation';

export default function Results(){
    const searchParams = useSearchParams();
    const data = searchParams.get('item');
    let jsonData = {"name": "", "url": ""};
    
    if (data == null) {
        // Safe to use 'data' here
        <div>Loading...</div>
    }
    else{
        jsonData = JSON.parse(data);
    }


    return (
        <div className={styles.container}>
            <Image className={styles.imageContainer}
                src={jsonData['url']}
                width={450}
                height={450}
                alt="Picture of the author"
            />
            <div className={styles.textcontainer} >
                <h1>Product Details</h1>
                <br />
                <h2>{jsonData['name']}</h2>
            </div>
            
        </div>
    );
}