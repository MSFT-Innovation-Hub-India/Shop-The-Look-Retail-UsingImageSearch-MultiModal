'use client'
import Image from 'next/image'
import Link from 'next/link'
import styles from './style.module.css'  // Assuming you have a CSS module
import { useRouter, useSearchParams } from 'next/navigation'
import { parse } from 'path'
import axios from 'axios'
import { useEffect } from 'react'
import { revalidatePath } from 'next/cache'

export default function Results() {
  const searchParams = useSearchParams()

  const data = searchParams.get('data');
  let jsonData = [];

  // console.log(data);

  if (data == null) {
    // Safe to use 'data' here
    <div>Loading...</div>
  }
  else{
    jsonData = JSON.parse(data);
  }

  console.log(data)
  console.log(jsonData)

  // let parsedData = null;
  // if (data) {
  //   try{
  //     parsedData = JSON.parse(decodeURIComponent(data as string));
  //   } catch (error) {
  //     console.log('Error parsing data: ', error);
  //   }
  // }

  useEffect(() => {
    axios.post('http://127.0.0.1:5328/api/speak', {
      text: "Absolutely! Here are some great options."
    }).then(function(response){
      console.log(response)
    }).catch(function(error){
      console.log(error)
    })
  }, [data])

    return (
      <div>
      <div className={styles.back_button}>
        <Link className='back-button' href={'/'}>
          <Image width="24" height="24" src="https://img.icons8.com/ios-filled/50/FFFFFF/home.png" alt="home--v1"/>
        </Link>
      </div>
      <div className={styles.imageContainer}>
      {jsonData.map((item, index) => (
        <Link key={index} href={`/info?item=${encodeURIComponent(JSON.stringify(item))}`}>
          <Image
            src={item.url}
            width={500}
            height={500}
            alt={`Picture ${index + 1}`}
          />
        </Link>
      ))}
    </div>
    </div>
    )
}
