import React, { useState } from 'react';
import { AiOutlineMenu, AiOutlineClose } from 'react-icons/ai';
import { Link } from 'react-router-dom';

//temp test data
const Clothes = [
  { id: 1, name: 'Red Boots', type: 'boots', colour: '#ff0000' },
  { id: 2, name: 'Blue Jacket', type: 'jackets', colour: '#0000ff' },
  { id: 3, name: 'Green Hat', type: 'hats', colour: '#00ff00' },
  { id: 4, name: 'Black Trainers', type: 'trainers', colour: '#000000' },
  { id: 5, name: 'White T-Shirt', type: 'tops', colour: '#ffffff' },
  { id: 6, name: 'Grey Trousers', type: 'trousers', colour: '#808080' },
  { id: 7, name: 'Pink Jacket', type: 'jackets', colour: '#ffc0cb' },
  { id: 8, name: 'Brown Boots', type: 'boots', colour: '#a52a2a' },
];

//consts
const Categories = ['all', 'boots', 'hats', 'jackets', 'tops', 'trainers', 'trousers'];
const Colours = {
  all: 'All',
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
  const [category, setCategory] = useState('all');
  const [color, setColor] = useState('all');
  const [search, setSearch] = useState('');

  const handleNav = () => setNav(!nav);

  const filteredItems = Clothes.filter(item => {
    const matchesCategory = category === 'all' || item.type === category;
    const matchesColor = color === 'all' || item.colour === color;
    const matchesSearch = item.name.toLowerCase().includes(search.toLowerCase());

    return matchesCategory && matchesColor && matchesSearch;
  });

  return (
    <div className="w-full h-screen bg-black relative text-white">
      <div className="flex justify-between items-center p-5">
        <h1 className="font-bold text-4xl text-center flex-1">
          Upload a photo and let AI do the rest
        </h1>

        <button
          className="rounded w-16 h-16 m-5 hover:scale-110 duration-200 flex items-center justify-center"
          onClick={handleNav}
        >
          {!nav ? <AiOutlineMenu size={40} /> : <AiOutlineClose size={40} />}
        </button>
      </div>

            {/* Menu */}
      <ul className={`fixed top-0 h-full w-[60%] bg-black transition-all duration-300 ${nav ? 'left-0' : '-left-full'}`}>
        <li className="p-4 uppercase text-4xl font-bold border-b border-gray-600">Menu:</li>
        <li className="p-4 uppercase text-2xl border-b border-gray-600">
          <Link to="/Upload">Upload</Link>
        </li>
        <li className="p-4 uppercase text-2xl border-b border-gray-600">
          <Link to="/Library">Library</Link>
        </li>
        <li className="p-4 uppercase text-2xl border-b border-gray-600">
          <Link to="/Outfits">Outfits</Link>
        </li>
        <li className="p-4 uppercase text-2xl border-b border-gray-600">
          <Link to="/Generate">Generate</Link>
        </li>
      </ul>


      <div className="relative z-10 p-5">
        <h2 className="text-2xl mb-4 font-semibold">Library</h2>

        <div className="grid md:grid-cols-3 gap-3 mb-6">
          <input
            type="text"
            placeholder="Search clothes..."
            value={search}
            //Sets search to the input
            onChange={(e) => setSearch(e.target.value)}
            className="p-2 rounded bg-black text-white border border-gray-600"
          />




          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="p-2 rounded bg-black text-white border border-gray-600"
          >
            {Categories.map(item => (
              <option key={item} value={item} className="text-black">
                {item.charAt(0).toUpperCase() + item.slice(1)}
              </option>
            ))}
          </select>



          <select
            value={color}
            onChange={(e) => setColor(e.target.value)}
            className="p-2 rounded bg-black text-white border border-gray-600"
          >
            {Object.entries(Colours).map(([hex, name]) => (
              <option key={hex} value={hex} className="text-black">
                {name}
              </option>
            ))}
          </select>
        </div>






        <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
          {(() => {
            if (filteredItems.length > 0) 
              {
              // items to display
              return filteredItems.map(item => (
                <div
                  key={item.id}
                  className= "bg-gray-800 hover:bg-gray-700 rounded-2xl p-4  hover:scale-105 transition"
                >
                  <div
                    className="w-full h-32 rounded-lg mb-3"
                    style={{ backgroundColor: item.colour }}
                  />
                  <h3 className="font-semibold text-lg">{item.name}</h3>
                  <p className="text-sm text-gray-400">{item.type}</p>
                </div>
              ));
            } 
            else 
            {
              // No items :(
              return <p className="text-gray-400">No items found.</p>;
            }
          })()}
        </div>
      </div>
    </div>
  );
};

export default Library;
