'use client'

import React, { useEffect, useState } from 'react'
import Link from 'next/link'
import { useHeader } from '../Header'

function Nav() {
    const { isShrunk } = useHeader();
  
    return (
      <div className={`fixed w-full transition-all duration-500 ${isShrunk ? 'bg-header py-2' : 'bg-header py-80'}`}>
        <div className='header flex w-80 mx-auto justify-between items-center'>
          <div className='logo'>
            <h2 className='text-4xl font-bold'>Shop the Look</h2>
          </div>
          <div className='menu'>
            <nav>
              <ul className='flex gap-4'>
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