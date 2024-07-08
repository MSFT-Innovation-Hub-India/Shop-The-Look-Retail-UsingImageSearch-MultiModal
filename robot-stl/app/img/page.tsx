import Image from 'next/image'
import Link from 'next/link'
import styles from './style.module.css'  // Assuming you have a CSS module

export default function Results() {
    return (
      <div className={styles.imageContainer}>
        <Link href="/info">
          <Image
            src="/one.jpg"
            width={500}
            height={500}
            alt="Picture of the author"
          />
        </Link>
        <Link href="/info">
          <Image
            src="/two.jpg"
            width={500}
            height={500}
            alt="Picture of the author"
          />
        </Link>
        <Link href="/info">
          <Image
            src="/three.jpg"
            width={500}
            height={500}
            alt="Picture of the author"
          />
        </Link>
      </div>
    )
}
