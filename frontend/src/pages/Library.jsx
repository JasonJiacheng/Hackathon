import React, { useState } from 'react';
import { AiOutlineMenu, AiOutlineClose } from 'react-icons/ai';
import { Link } from 'react-router';

const Categories = ['boots', 'hats', 'jackets', 'tops', 'trainers', 'trousers'];

const Colours = {
  '#ff0000': 'Red',
  '#ffff00': 'Yellow',
  '#0000ff': 'Blue',
  '#00ff00': 'Green',
  '#ffa500': 'Orange',
  '#800080': 'Purple',
  '#ffc0cb': 'Pink',
  '#a52a2a': 'Brown',
  '#000000': 'Black',
  '#ffffff': 'White',
  '#808080': 'Grey',
};

const Library = () => {
  const [nav, setNav] = useState(false);
  const [category, setCategory] = useState('');
  const [color, setColor] = useState('');

  const handleNav = () => setNav(!nav);

  return (
    <div className="w-full h-screen bg-black relative">

      {/* Header */}
      <div className="flex justify-between items-center p-5">
        <h1 className="font-bold text-white text-4xl text-center flex-1">
          Upload a photo and let AI do the rest
        </h1>

        <button
          className="rounded w-16 h-16 m-5 text-white hover:scale-110 duration-200 flex items-center justify-center"
          onClick={handleNav}
        >
          {!nav ? <AiOutlineMenu size={40} /> : <AiOutlineClose size={40} />}
        </button>
      </div>

      {/* Menu */}
      <ul className={`fixed top-0 h-full w-[60%] bg-black transition-all duration-300 ${nav ? "left-0" : "-left-full"}`}>
        <li className="p-4 uppercase text-white text-4xl font-bold">Menu:</li>

        <li className="p-4 uppercase text-white text-2xl border-b border-gray-600">
          <Link to="/Upload">Upload</Link>
        </li>

        <li className="p-4 uppercase text-white text-2xl border-b border-gray-600">
          <Link to="/Library">Library</Link>
        </li>

        <li className="p-4 uppercase text-white text-2xl border-b border-gray-600">
          <Link to="/Outfits">Outfits</Link>
        </li>

        <li className="p-4 uppercase text-white text-2xl border-b border-gray-600">
          <Link to="/Generate">Generate</Link>
        </li>
      </ul>

      {/* Content */}
      <div className="relative z-10 p-5">

        <h2 className="text-white text-2xl mb-4">Library</h2>

        <input
          type="text"
          placeholder="Search clothes"
          className="block m-2 p-2 bg-white text-black rounded"
        />

        {/* Category Dropdown */}
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="block m-2 p-2 bg-white text-black rounded"
        >
          <option value="">Type</option>
          {Categories.map(item => (
            <option key={item} value={item}>
              {item}
            </option>
          ))}
        </select>

        {/* Colour Dropdown */}
        <select
          value={color}
          onChange={(e) => setColor(e.target.value)}
          className="block m-2 p-2 bg-white text-black rounded"
        >
          <option value="">Select colour</option>
          {Object.entries(Colours).map(([hex, name]) => (
            <option key={hex} value={hex}>
              {name}
            </option>
          ))}
        </select>

      </div>

    </div>
  );
};

export default Library;