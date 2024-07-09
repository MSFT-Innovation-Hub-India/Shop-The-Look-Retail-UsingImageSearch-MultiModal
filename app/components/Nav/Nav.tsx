'use client'

import React, { useEffect, useState } from 'react'
import Link from 'next/link'

function Nav() {
    const [header, setHeader] = useState(false)

    const scrollHeader = () => {
        if (window.scrollY >= 20) {
            setHeader(true)
        } else {
            setHeader(false)
        }
    }

    useEffect(() => {
        window.addEventListener('scroll', scrollHeader)
        return () => {
            window.removeEventListener('scroll', scrollHeader)
        }
    }, [])

    return (
        <div className={`fixed w-full transition-all duration-500 ${header ? 'text-white bg-pink-950 py-2' : 'bg-pink-200 py-80'}`}>
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
    )
}

export default Nav
