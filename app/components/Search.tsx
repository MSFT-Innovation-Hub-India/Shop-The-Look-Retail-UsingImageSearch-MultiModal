import React from 'react'
import { FaMicrophone } from 'react-icons/fa'
import { IoSend } from 'react-icons/io5'
import { MdOutlineFileUpload } from 'react-icons/md'

export const Searchbar = () => {
    return (
      <form className='w-[300px] mx-auto relative'>
        <div className="flex justify-center">
            <input
              type="search"
              placeholder='How can I help'
              className='fixed bottom-11 w-[80%] p-4 rounded-3xl bg-slate-800'
            />
            <button className='fixed bottom-11 p-4 bg-transparent right-[120px]'>
              <FaMicrophone  color='#1E293B' size={25} />
            </button>
            <button className='fixed bottom-10 p-4 bg-transparent right-[182px]'>
              <IoSend  color='white' size={30} />
            </button>
            <button className='fixed bottom-10 p-4 bg-transparent right-[80px]'>
              <MdOutlineFileUpload color='#1E293B' size={35} />
            </button>
          </div>
      </form>
    )
  }
  
