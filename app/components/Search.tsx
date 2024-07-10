<meta name="viewport" content="width=device-width, initial-scale=1.0"></meta>

import React from 'react'
import { FaMicrophone } from 'react-icons/fa'
import { IoSend } from 'react-icons/io5'
import { MdAddPhotoAlternate } from 'react-icons/md'

export const Searchbar = () => {
    return (
      <form className='w-[300px] mx-auto relative'>
        <div className="flex justify-center">
            <input
              type="search"
              placeholder='How can I help'
              className='fixed bottom-11 w-[60%] p-4 rounded-3xl bg-slate-800'
            />
            <button className='fixed bottom-11 p-4 bg-transparent right-[245px]'>
              <FaMicrophone  color='#1E293B' size={30} />
            </button>
            <button className='fixed bottom-10 p-4 bg-transparent right-[345px]'>
              <IoSend color='white' size={30} />
            </button>
            <button className='fixed bottom-10 p-4 bg-transparent right-[280px]'>
              <MdAddPhotoAlternate color='#1E293B' size={37} />
            </button>
          </div>
      </form>
    )
  }
  
