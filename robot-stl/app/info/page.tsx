import Image from 'next/image';
import Link from 'next/link';
import styles from './style.module.css';

interface ResultsProps {
}

const Results: React.FC<ResultsProps> = ({}) => {
    return (
        <div className={styles.container}>
            <Image className={styles.imageContainer}
                src="/one.jpg"
                width={500}
                height={500}
                alt="Picture of the author"
            />
            <div className={styles.textcontainer} >
                <h1>Product Name</h1>
                <h2>Price: $100</h2>
                <h3>Aisle: 2B</h3>

                <div className={styles.buttonsContainer}>
                <Link legacyBehavior href="/details">
                    <a className={styles.button}>Tell me more</a>
                </Link>
                <Link legacyBehavior href="/">
                    <a className={styles.button}>Take me there</a>
                </Link>
                </div>

            </div>
        </div>
    );
}

export default Results;