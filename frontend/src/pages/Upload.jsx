import React, { useState } from 'react';
import { AiOutlineMenu, AiOutlineClose } from 'react-icons/ai';
import {Link} from 'react-router'

const Upload = () => {
  const [nav, setNav] = useState(false);
  const [file, setFile] = useState(false);

  const handleFile = () => {};
  const handleNav = () => setNav(!nav);

  return (
    <div className="w-full h-screen bg-black">

      {/* Left pane --> Menu button */}
      <div className="flex justify-between items-center p-5">
        <h1 className = "font-bold text-white text-4xl text-center flex-1"> Upload a photo and let AI do the rest </h1>
        <button
          className="rounded w-16 h-16 m-5 text-white hover:scale-110 duration-200 flex items-center justify-center"
          onClick={handleNav}>
          {!nav ? <AiOutlineMenu size={40} /> : <AiOutlineClose size={40} />}
        </button>
      </div>

      {/* Main grid */}
      <div className="grid grid-cols-2 h-130">

        {/* Left panel */}
        <div className="bg-black flex p-4">
          <div className="bg-white rounded-md flex-1"></div>
        </div>

        {/* Right panel */}
        <div className="bg-black p-4 grid grid-rows-2 gap-4">

          {/* Form grid of 2 columns */}
          <div className="bg-black grid grid-cols-2 gap-4 text-white">
            <p className="font-bold text-xl">Name</p>
            <input type="text" className="bg-white rounded w-full px-2 py-1" />
            <p className="font-bold text-xl">Category</p>
            <input type="text" className="bg-white rounded w-full px-2 py-1" />
          </div>

          {/* Upload button */}
          <div className="flex justify-center items-center bg-black">
            <button
                className="rounded-md text-black bg-blue-400 font-bold text-2xl hover:scale-105 transition-transform duration-150 px-8 py-4 w-48">
                Upload
            </button>
          </div>

        </div>
      </div>

        {/* Menu */}
        <ul className = {nav ? "fixed top-0 left-0 w-[60%] h-full border-r border-gray-600 bg-black transition-in-out duration-300" : 
                                   "transition-in-out duration-300 fixed -left-full"}>
            <li className = "p-4 uppercase text-white text-2xl border-b border-gray-600">
                <Link to = "Upload" > Upload </Link> 
            </li>

            <li className = "p-4 uppercase text-white text-2xl border-b border-gray-600">
                <Link to = "Library" > Library </Link> 
            </li>

            <li className = "p-4 uppercase text-white text-2xl border-b border-gray-600">
                <Link to = "Outfits" > Outfits </Link> 
            </li>

            <li className = "p-4 uppercase text-white text-2xl border-b border-gray-600">
                <Link to = "Generate" > Generate </Link> 
            </li>
        </ul>
      
    </div>
  );
};

export default Upload;
