import Image from "next/image";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="image-animation-container">
        <Image src="/close.png" alt="Image 1" layout="fill" className="image-animation image1"/>
        <Image src="/open.png" alt="Image 2" layout="fill" className="image-animation image2"/>
      </div>
      {/* Rest of your component */}
    </main>
  );
}
