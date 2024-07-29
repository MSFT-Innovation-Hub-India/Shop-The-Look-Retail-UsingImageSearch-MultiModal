'use client'

import React from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { useHeader } from '../Header'

function Nav() {
    const { isShrunk } = useHeader();
  
    return (
      <div className={`fixed w-full transition-all duration-500 ${isShrunk ? 'text-black bg-header py-2' : 'text-black bg-header py-80'}`}>
        <div className='header flex w-80 mx-auto justify-between items-center'>
          <div className='logo duration-500'>
          {isShrunk ? (
            <Image 
            src='/newlogo.png' 
            alt='New Logo' 
            width={370}
            height={370}/>
          ) : (
            <h2 className='text-5xl font-bold pr-12'>Shop the Look</h2>
          )}
          </div>
          <div className='menu'>
            <nav>
              <ul className='flex gap-4 pr-3'>
                <li>
                  <Link href='/'>Home</Link>
                </li>
                <li>
                  <Link href='/'>History</Link>
                </li>
                <li>
                  <Link href='/'>Explore</Link>
                </li>
              </ul>
            </nav>
          </div>
        </div>
      </div>
    );
  }
  
  export default Nav;