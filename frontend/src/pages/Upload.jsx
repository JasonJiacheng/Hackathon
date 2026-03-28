import React, { useState, useRef } from 'react';
import { AiOutlineMenu, AiOutlineClose } from 'react-icons/ai';
import {Link} from 'react-router'
import DefaultImage from "../assets/closet.png"

const Upload = () => {
  const [nav, setNav] = useState(false);
  const [file, setFile] = useState(null);
  const fileUploadRef = useRef();

  // Default image
  const [avatar, setAvatar] = useState(DefaultImage);

  // Event handlers
  const handleNav = () => setNav(!nav);

  const uploadImageDisplay = () => {
    const uplaodedFile = fileUploadRef.current.files[0];
    const cachedURL = URL.createObjectURL(uplaodedFile);
    setAvatar(cachedURL);
  }

  return (
    <div className="w-full h-screen bg-black ">

      {/* Upper pane --> Menu button */}
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
        <div className="bg-black py-4 px-8">
          {/* <div className="bg-white rounded-md flex-1"></div> */}
          <img src = {avatar} alt = "avatar" className = "rounded-md w-full flex-auto"></img>
        </div>

        {/* Right panel */}
        <div className="bg-black pr-4 py-8 grid grid-rows-2 gap-4">

          {/* Form grid of 2 columns */}
          <div className="bg-black grid grid-cols-2 gap-4 text-white">
            <p className="font-bold text-xl">Name</p>
            <input type="text" className="bg-white rounded w-full px-2 py-1" />
            <p className="font-bold text-xl">Category</p>
            <input type="text" className="bg-white rounded w-full px-2 py-1" />
          </div>

          {/* Upload button */}
          <div className="flex flex-col justify-center items-center bg-black ">
            <form id = "form" encType="multipart/form-data" className = "bg-green-300 w-30 text-center h-20 rounded-md hover:scale-105 transition-transform duration-300">
                <label htmlFor="inputButton" className = "text-black font-bold text-2xl">
                    Upload
                </label> 
                <input id = "inputButton" type = "file" className = "hidden" ref = {fileUploadRef} accept = "image/*" onChange={uploadImageDisplay}>
                </input>
            </form>
          </div>

        </div>
      </div>

        {/* Menu */}
        <ul className={`fixed top-0 h-full w-[60%] bg-black transition-all duration-300 ease-in-out ${nav ? "left-0" : "-left-full"}`}>
            <li className = "p-4 uppercase text-white text-4xl font-bold"> Menu: </li>
                                    
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
