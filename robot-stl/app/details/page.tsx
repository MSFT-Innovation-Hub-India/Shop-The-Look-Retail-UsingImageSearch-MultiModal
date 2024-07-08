import Image from 'next/image'

export default function Results() {
    return (
      <div>
        <Image
        src="/one.jpg"
        width={500}
        height={500}
        alt="Picture of the author"
        />
        <h1>Product Name</h1>
        <p>Price: </p>
        <p>Aisle: </p>
      </div>
    )
}