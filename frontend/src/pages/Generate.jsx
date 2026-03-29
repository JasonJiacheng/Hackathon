import React from 'react';
import { useState, useRef } from 'react';
import { AiOutlineMenu, AiOutlineClose } from 'react-icons/ai';
import {Link} from 'react-router-dom';
import image from '../assets/closet.png'

const Generate = () => {
    const [nav, setNav] = useState(false);
    // Event handlers
    const handleNav = () => setNav(!nav);
    // Current category dragged
    const [category, setCategory] = useState('');
    const handleCategory = (item) => {
        setCategory(item);
    };

    // Categories
    const Categories = ['shoes', 'shirts', 'outerwear', 't-shirts', 'shorts', 'trousers', "dresses"];


    return (
        <div className="relative bg-black bg-cover bg-center h-screen" style={{ backgroundImage: `url(${image})` }}>
            {/* Upper pane --> Menu button */}
            <div className="flex justify-between items-center p-5">
                <h1 className = "font-bold text-white text-4xl text-center flex-1"> Upload a photo and let AI do the rest </h1>
                <button
                className="rounded w-16 h-16 m-5 text-white hover:scale-110 duration-200 flex items-center justify-center"
                onClick={handleNav}>
                <AiOutlineMenu size={40} />
                </button>
            </div>


            {/* Buttons */}
            <div className = "flex justify-center overflow-x-auto py-3 space-x-4 mx-4">
                {Categories.map((item) => (
                    <button key = {item} onClick = {() => handleCategory(item)}
                        className = "bg-white w-50 text-center h-20 rounded-md hover:scale-105 hover:bg-gray-200 transition-transform duration-300 text-black font-bold text-2xl">
                        {item}
                    </button>
                ))}

            </div>

            {/* Drag and drop containers */}
            <div className = "flex flex-row gap-4 h-80 bg-white mx-10">

                <div className = "flex flex-1 relative ">


                </div>

                <div className = " flex flex-1 relative">


                </div>

            </div>

            {/* Generate button */}
            <div className = "flex justify-center py-8">
                <button className = "text-bold text-2xl font-bold rounded-md bg-white w-50 h-15 hover:bg-gray-200 hover:scale-105 transition-transform duration-300">
                    Generate
                </button>
            </div>

            {/* Popup */}

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
                                            
                    <li className = "p-4 uppercase text-white text-2xl border-b border-gray-600">
                        <Link to = "/Upload" > Upload </Link> 
                    </li>

                    <li className = "p-4 uppercase text-white text-2xl border-b border-gray-600">
                        <Link to = "/Library" > Library </Link> 
                    </li>

                    <li className = "p-4 uppercase text-white text-2xl border-b border-gray-600">
                        <Link to = "/Outfits" > Outfits </Link> 
                    </li>

                    <li className = "p-4 uppercase text-white text-2xl border-b border-gray-600">
                        <Link to = "/" > Home </Link> 
                    </li>
                </ul>
            
            </div>
  )
}

export default Generate
