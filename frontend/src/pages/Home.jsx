import React from 'react'
import {AiOutlineMenu, AiOutlineClose} from 'react-icons/ai'

const Home = () => {
    // for the menu
    const [nav, setNav] = useState(false);    


    // Event handler
    const handleNav = () => {
        setNav(!nav);
    }
  
    return (
        // Main container
        <div className = "">
            {/* Button to navigate to the menu (we want to change to close) -> appears only on phones */}
            <button onClick={handleNav} className = "block md:hidden">
                {!nav ? <AiOutlineMenu size = {20}></AiOutlineMenu>
                    : <AiOutlineClose size = {20}></AiOutlineClose>}
            </button>

            {/* Actual menu / Navigation menu*/}
            <div className = {!nav ? "fixed left-[-100%]" 
                              : "fixed left-0 top-0 h-full w-[60%] ease-in-out duration-500 bg-[#000300]"}>
                {/* Name of the application*/}
                <h1 className = "w-full text-3xl font-bold text-[#00df9a] m-4"> REACT. </h1>

                {/* List of items in the menu */}
                <ul className = 'p-4 uppercase'>
                <li className = 'p-4 border-b border-gray-600'> Home </li>
                <li className = 'p-4 border-b border-gray-600'> Company </li>
                <li className = 'p-4 border-b border-gray-600'> Ressources </li>
                <li className = 'p-4 border-b border-gray-600'> About </li>
                <li className = 'p-4 border-b border-gray-600'> Contact </li>
                </ul>
            </div>
        </div>
    );
}

export default Home
