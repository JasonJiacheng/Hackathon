import {useState} from 'react';
import {AiOutlineMenu, AiOutlineClose} from 'react-icons/ai';
import {Link} from 'react-router'


const Home = () => {
    // for the menu
    const [nav, setNav] = useState(false);      // when false menu button


    // Event handler
    const handleNav = () => {
        setNav(!nav);
    }
  
    return (
        <div className = "relative bg-black">
            <div className = "flex justify-end">
                <button className = "rounded w-16 h-16 m-5 text-white hover:scale-110 duration-200 flex items-center justify-center " 
                        onClick = {handleNav}>
                    {!nav ? <AiOutlineMenu size = {200}/> : <AiOutlineClose size = {200}/>}
                </button>
            </div>

            <div className = "flex flex-col justify-center text-center">
                <h1 className = "text-white text-5xl font-bold"> Application Name</h1>

                {/* Live typing content */}
                {/* <div className = "flex items-center">
                    <ReactTyped className = "text-2xl font-bold py-2"
                        strings = {["Don't know what to wear or just bored to pick?"]} 
                        typeSpeed = {120}
                        backSpeed={120}
                        loop/>
                </div> */}
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
}

export default Home