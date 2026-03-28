import React from 'react';
import { useState, useRef } from 'react';
import { AiOutlineMenu, AiOutlineClose } from 'react-icons/ai';
import {Link} from 'react-router';

const Generate = () => {
    const [nav, setNav] = useState(false);
    // Event handlers
    const handleNav = () => setNav(!nav);
    return (
        <div>
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

                {/* Menu */}
                <ul className={`fixed top-0 h-full w-[60%] bg-black transition-all duration-300 ease-in-out ${nav ? "left-0" : "-left-full"}`}>
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
                        <Link to = "/Generate" > Generate </Link> 
                    </li>
                </ul>
            
            </div>
        
        </div>
  )
}

export default Generate
