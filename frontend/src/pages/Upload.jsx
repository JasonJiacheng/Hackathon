import React, { useState, useRef } from 'react';
import { AiOutlineMenu, AiOutlineClose } from 'react-icons/ai';
import {Link} from 'react-router-dom';
import DefaultImage from "../assets/closet.png";
import { apiPost } from '../api.js';

const Upload = () => {
  const [nav, setNav] = useState(false);
  const [file, setFile] = useState(null);
  const fileUploadRef = useRef();
  const [name, setName] = useState('no-name');
  const [category, setCategory] = useState('no-category');
  const [detectedType, setDetectedType] = useState(null);
  const [detectedColour, setDetectedColour] = useState(null);

  // Default image
  const [avatar, setAvatar] = useState(DefaultImage);

  // Event handlers
  const handleNav = () => setNav(!nav);
  const handleCategory = (e) => setCategory(e.target.value);
  const handleName = (e) => setName(e.target.value);

  const uploadImageDisplay = () => {
    const uplaodedFile = fileUploadRef.current.files[0];
    const cachedURL = URL.createObjectURL(uplaodedFile);
    setAvatar(cachedURL);
    setFile(uplaodedFile);
  }



  // Take image to the backend
  const handleSubmit = (event) => {
    event.preventDefault();

  if (!file) {                          // ← add this check
    alert('Please choose a file first');
    return;
  }

  const data = new FormData();
  data.append('image', file);
  data.append('name', name);
  data.append('category', category);

  fetch('http://localhost:5000/api/upload', {
    method: 'POST',
    body: data
  })
  .then(res => res.json())
  .then(data => {
    setDetectedType(data.category);
    setDetectedColour(data.detected_colour);
  })
  .catch(err => console.error('Upload failed', err));
     
  }

  return (
    <div className="w-full h-screen bg-black ">

      {/* Upper pane --> Menu button */}
      <div className="flex justify-between items-center p-5">
        <h1 className = "font-bold text-white text-4xl text-center flex-1"> Upload a photo and let AI do the rest </h1>
        <button
          className="rounded w-16 h-16 m-5 text-white hover:scale-110 duration-200 flex items-center justify-center"
          onClick={handleNav}>
          <AiOutlineMenu size={40} /> 
        </button>
      </div>

      {/* Main grid */}
      <div className="grid grid-cols-2 h-130">

        {/* Left panel */}
        <div className="bg-black py-4 px-8">
          {/* <div className="bg-white rounded-md flex-1"></div> */}
          <img src = {avatar} alt = "avatar" className = "rounded-md h-full flex-auto"></img>
        </div>

        {/* Right panel */}
        <div className="bg-black pr-4 py-8 grid grid-rows-2 gap-4">

          {/* Form grid of 2 columns */}
          <div className="bg-black grid grid-cols-2 gap-4 pr-16 text-white">
            <p className="font-bold text-3xl">Name</p>
            <input type="text" onChange={handleName} className="bg-white text-black text-2xl rounded w-full px-2 py-1" />
            <p className="font-bold text-3xl">Category</p>
            <select className="bg-white rounded w-full px-2 py-1 text-black text-2xl" onChange={handleCategory}>
                <option value="">Select category</option>
                <option value="shirt"> Shirt</option>
                <option value="shoes"> Shoes</option>
                <option value="shorts"> Shorts</option>
                <option value="skirt"> Skirt</option>
                <option value="t-shirt"> Vegetable</option>
                <option value="trousers"> Dairy</option>
                <option value="outerwear"> Outerwear</option>
            </select>
          </div>
          

          {/* Upload button */}
          <div className="flex justify-center items-center  bg-black ">
            <form id = "form" onSubmit = {handleSubmit} encType="multipart/form-data" className = "flex flex-row justify-center items-center gap-4">
           
                {/* to show */}
                <label htmlFor="inputButton" className="text-bold text-2xl font-bold rounded-md bg-white w-50 h-15 flex items-center justify-center hover:bg-gray-200 hover:scale-105 transition-transform duration-300">
                    Choose File
                </label>
                <input id="inputButton" type="file" className="hidden" ref={fileUploadRef} accept="image/*" onChange={uploadImageDisplay} />

                {/* to store */}
                <button type="submit" className="text-bold text-2xl font-bold rounded-md bg-white w-50 h-15 flex items-center justify-center hover:bg-gray-200 hover:scale-105 transition-transform duration-300">
                    Submit
                </button>
                {detectedType && detectedColour && (
                  <p className="text-white text-3xl font-bold mt-4">
                    {detectedColour.charAt(0).toUpperCase() + detectedColour.slice(1)} {detectedType}
                  </p>
)}
            
            </form>
          </div>

        </div>
      </div>

        {/* Menu */}
        <ul className={`fixed top-0 h-full w-full bg-black transition-all duration-300 ease-in-out ${nav ? "left-0" : "-left-full"}`}>
            {/* Close button */}
                <div className="flex justify-end p-5">
                    <button
                        onClick={handleNav}
                        className="text-white hover:scale-110 duration-200"
                    >       
                    <AiOutlineClose size={40} />
                    </button>
                </div>
        
            <li className = "p-4 uppercase text-white text-4xl font-bold"> Menu: </li>
                                    
            <li className = "p-4 uppercase text-white text-2xl border-b border-gray-600 hover:scale-105 hover:text-gray-600 duration-200">
                <Link to = "/" > Home </Link> 
            </li>

            <li className = "p-4 uppercase text-white text-2xl border-b border-gray-600 hover:scale-105 hover:text-gray-600 duration-200">
                <Link to = "/Library" > Library </Link> 
            </li>

            <li className = "p-4 uppercase text-white text-2xl border-b border-gray-600 hover:scale-105 hover:text-gray-600 duration-200">
                <Link to = "/Outfits" > Outfits </Link> 
            </li>

            <li className = "p-4 uppercase text-white text-2xl border-b border-gray-600 hover:scale-105 hover:text-gray-600 duration-200">
                <Link to = "/Generate" > Generate </Link> 
            </li>
        </ul>
      
    </div>
  );
};

export default Upload;
