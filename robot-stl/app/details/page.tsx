import Image from 'next/image';
import styles from './style.module.css';

interface ResultsProps {
}

const Results: React.FC<ResultsProps> = ({}) => {
    return (
        <div className={styles.container}>
            <Image className={styles.imageContainer}
                src="/one.jpg"
                width={450}
                height={450}
                alt="Picture of the author"
            />
            <div className={styles.textcontainer} >
                <h1>Product Details</h1>
                <br />
                <h2>Lorem ipsum, dolor sit amet consectetur adipisicing elit. Neque deleniti nulla distinctio exercitationem 
                    obcaecati mollitia magni voluptas, omnis quaerat consequatur illum voluptatum ratione voluptates ea molestias autem, tenetur nemo. 
                    Sapiente?</h2>
            </div>
            
        </div>
    );
}

export default Results;