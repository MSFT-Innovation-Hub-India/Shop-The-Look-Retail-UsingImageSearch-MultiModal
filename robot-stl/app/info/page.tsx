'use client'
import Image from 'next/image';
import Link from 'next/link';
import styles from './style.module.css';
import { useSearchParams } from 'next/navigation';
import { json } from 'stream/consumers';
import { useRouter } from 'next/navigation';

export default function Details(){
    const searchParams = useSearchParams();
    const data = searchParams.get('item');
    let jsonData = {"id": 0,"name": "", "url": "", "price": ""};
    console.log(data)

    const router = useRouter();
    
    if (data == null) {
        // Safe to use 'data' here
        <div>Loading...</div>
      }
      else{
        jsonData = JSON.parse(data);
      }

    return (
        <div className={styles.container}>
            <div className={styles.back_button}>
                <button className='back-button' onClick={() => router.back()} style={{ background: `url(${"https://img.icons8.com/sf-black/64/FFFFFF/back.png"}) no-repeat left center`, width:50, height:50 }}></button>
            </div>
            <Image className={styles.imageContainer}
                src={jsonData['url']}
                width={500}
                height={500}
                alt="Picture of the author"
            />
            <div className={styles.textcontainer} >
                <h2>Price: {jsonData['price']}</h2>
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