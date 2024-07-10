'use client'
import Image from 'next/image';
import styles from './style.module.css';
import { useSearchParams, useRouter } from 'next/navigation';

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

    const router = useRouter();

    return (
        <div className={styles.container}>
            <div className={styles.back_button}>
                <button className='back-button' onClick={() => router.back()} style={{ background: `url(${"https://img.icons8.com/sf-black/64/FFFFFF/back.png"}) no-repeat left center`, width:50, height:50 }}></button>
            </div>
            <div className={styles.imageContainer}>
            <Image className={styles.imageStyle}
                src={jsonData['url']}
                alt="Picture of the author"
                width={100}
                height={100}

            />
            </div>
            <div className={styles.textcontainer} >
                <h1>Product Details</h1>
                <br />
                <h2>{jsonData['name']}</h2>
            </div>
            
        </div>
    );
}