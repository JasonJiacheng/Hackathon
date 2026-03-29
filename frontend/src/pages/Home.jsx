import {useState} from 'react';
import {AiOutlineMenu, AiOutlineClose} from 'react-icons/ai';
import {Link} from 'react-router-dom'
import image from '../assets/closet.png'
import { ReactTyped } from 'react-typed';


const Home = () => {
    // for the menu
    const [nav, setNav] = useState(false);      // when false menu button
    const [steps, setSteps] = useState(0);


    // Event handler
    const handleNav = () => {
        setNav(!nav);
    }
  
    return (
        <div className="relative bg-black bg-cover bg-center h-screen" style={{ backgroundImage: `url(${image})` }}>
            <div className = "flex justify-end">
                <button className = "rounded w-16 h-16 m-5 text-white hover:scale-110 duration-200 flex items-center justify-center " 
                        onClick = {handleNav}>
                    <AiOutlineMenu size = {200}/> 
                </button>
            </div>

            <div className = "relative z-10 flex flex-col justify-center items-center text-center">
                <h1 className = "text-white text-7xl font-bold"> AI Outfit Generator </h1>

                {/* Live typing content */}
                <div className="text-white text-2xl md:text-3xl font-semibold m-20">
                    {steps == 0 && <ReactTyped
                    strings={[
                        "Don't know what to wear?"
                    ]}
                    typeSpeed= {50}      // typing speed in ms
                    loopCount = {1}              // loop infinitely
                    showCursor = {false}
                    onComplete = {() => setSteps(1)}
                    />}
                    {steps == 1 && <ReactTyped
                    strings={[
                        "Bored of having to pick outfits?"
                    ]}
                    showCursor = {false}
                    typeSpeed={50}      // typing speed in ms
                    loopCount = {1}              // loop infinitely
                    onComplete={() => setSteps(2)}
                    />}
                    {steps == 2 && <ReactTyped
                    strings={[
                        "Sit back and let AI decide your outfit for you!"
                    ]}
                    showCursor = {false}
                    typeSpeed={50}      // typing speed in ms
                    loopCount = {1}              // loop infinitely
                    onComplete = {() => setSteps(0)}
                    />}
                </div>
            </div>

            {/* Menu */}
            <ul className = {nav ? "fixed top-0 left-0 z-50 w-full h-full border-r border-gray-600 bg-black transition-in-out duration-300" : 
                                   "transition-in-out duration-300 fixed -left-full"}>
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

                <li className = "p-4 uppercase text-white text-2xl border-b hover:scale-105 hover:text-gray-600 duration-200 border-gray-600">
                    <Link to = "/Upload"> Upload </Link> 
                </li>

                <li className = "p-4 uppercase hover:scale-105 hover:text-gray-600 duration-200 text-white text-2xl border-b border-gray-600">
                    <Link to = "/Library" > Library </Link> 
                </li>

                <li className = "p-4 uppercase hover:scale-105 hover:text-gray-600 duration-200 text-white text-2xl border-b border-gray-600">
                    <Link to = "/Outfits" > Outfits </Link> 
                </li>

                <li className = "p-4 uppercase hover:scale-105 hover:text-gray-600 duration-200 text-white text-2xl border-b border-gray-600">
                    <Link to = "/Generate" > Generate </Link> 
                </li>
            </ul>
        </div>
    );
}

export default Home