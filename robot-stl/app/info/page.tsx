'use client'
import Image from 'next/image';
import Link from 'next/link';
import styles from './style.module.css';
import { useSearchParams } from 'next/navigation';
import { json } from 'stream/consumers';

export default function Details(){
    const searchParams = useSearchParams();
    const data = searchParams.get('item');
    let jsonData = {"name": "", "url": ""};
    console.log(data)
    
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
                width={500}
                height={500}
                alt="Picture of the author"
            />
            <div className={styles.textcontainer} >
                <h2>Price: Rs. 2499</h2>
                <h3>Aisle: 2B</h3>

                <div className={styles.buttonsContainer}>
                <Link legacyBehavior href={`/details?item=${encodeURIComponent(JSON.stringify(jsonData))}`}>
                    <a className={styles.button}>Tell me more</a>
                </Link>
                <Link legacyBehavior href={`/takemethere?item=${encodeURIComponent(JSON.stringify(jsonData))}`}>
                    <a className={styles.button}>Take me there</a>
                </Link>
                </div>

            </div>
        </div>
    );
}