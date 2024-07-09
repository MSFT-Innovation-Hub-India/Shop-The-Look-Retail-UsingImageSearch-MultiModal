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
              className='fixed bottom-10 w-[80%] p-4 rounded-full bg-slate-800'
            />
            <button>
              <FaMicrophone />
            </button>
            <button className='fixed bottom-10 mr- p-4'>
              <IoSend />
            </button>
            <button>
              <MdOutlineFileUpload />
            </button>
          </div>
      </form>
    )
  }
  
