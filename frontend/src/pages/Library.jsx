import React, { useEffect, useState } from 'react';
import { AiOutlineMenu, AiOutlineClose } from 'react-icons/ai';
import { Link } from 'react-router-dom';

// Temporary test data
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

const Categories = ['all', 'shoes', 'shirts', 'outerwear', 't-shirts', 'shorts', 'trousers', "dresses"];

const Colours = {
    all : "All",
    "#ff0000": "Red",
    "#ffff00": "Yellow",
    "#0000ff": "Blue",
    "#00ff00": "Green",
    "#ffa500": "Orange",
    "#800080": "Purple",
    "#ffc0cb": "Pink",
    "#a52a2a": "Brown",
    "#000000": "Black",
    "#ffffff": "White",
    "#808080": "Grey",
    "#000080": "Navy",
    "#6b6b2a": "Olive",
}

const Library = () => {
  // Navigation
  const [nav, setNav] = useState(false);

  // Sliders
  const [category, setCategory] = useState('all');
  const [color, setColor] = useState('all');
  const [search, setSearch] = useState('');

  const handleNav = () => setNav(!nav);

  // Loading the images
  const [images, setImages] = useState([]);   // each item is a dictionary of name and url

  // Fetch them on load using the urls we have created from the server (we need the posrt of the server)
  useEffect(() => {
    fetch('http://localhost:3000/api/images')
    .then(res => res.json())
    .then(data => setImages(data))
    .catch(err => console.log(err))
  }, []);

  return (
    <div className="w-full min-h-screen bg-black text-white">
      {/* menu and button */}
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

      {/* Placeholders */}
      <div className="relative z-10 p-5">

        <div className="grid md:grid-cols-3 gap-3 mb-6">
          <input
            type="text"
            placeholder="Search clothes by name ..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="p-2 rounded bg-black text-white border border-gray-600"
          />

          <div className="flex overflow-x-auto py-2 space-x-2 border border-gray-600 rounded p-2 bg-black">
          {Categories.map(cat => (
              <button
                key={cat}
                onClick={() => setCategory(cat)}
                className={`px-4 py-2 rounded text-white whitespace-nowrap border border-gray-600 transition
                  ${category === cat ? 'bg-gray-700' : 'bg-black hover:bg-gray-800'}
                `}
              >
                {cat.charAt(0).toUpperCase() + cat.slice(1)}
              </button>
            ))}
          </div>

          <div className="flex overflow-x-auto py-2 space-x-2 border border-gray-600 rounded p-2 bg-black">
          {Object.values(Colours).map(cat => (
              <button
                key={cat}
                onClick={() => setColor(cat)}
                className={`px-4 py-2 rounded text-white whitespace-nowrap border border-gray-600 transition
                  ${color === cat ? 'bg-gray-700' : 'bg-black hover:bg-gray-800'}
                `}
              >
                {cat.charAt(0).toUpperCase() + cat.slice(1)}
              </button>
            ))}
          </div>
        </div>

        <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
            {images.length > 0 ?   // Ensure we have at least one image
            images.filter (item => {
                const type = item.name.split('-')[0];

                const matchesCategory =
                  category === 'all' || type === category;

                const matchesSearch =
                  item.name.toLowerCase().includes(search.toLowerCase());

                return matchesCategory && matchesSearch; 
              })
            .map(item => (
              <div
                key={item.name}
                className="bg-gray-800 hover:bg-gray-700 rounded-2xl p-4 hover:scale-105 transition-transform"
              >
                <div
                  className="w-full h-32rounded-lg mb-3"
                >
                  <img
                    src={item.url}
                    className="w-full object-contain rounded-md"
                  />
                </div>
                <h3 className="font-semibold text-lg">{item.name.split('-')[0]}</h3>
              </div>
            )) : (
            <p className="text-gray-400">No items found.</p>
          )}
        </div>
      </div>

      {/* Menu */}
      <ul
        className={`fixed top-0 left-0 h-full w-full bg-black z-50 shadow-lg transition-all duration-300 ${
          nav ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex justify-end p-5">
          <button onClick={handleNav} className="text-white hover:scale-110 duration-200">
            <AiOutlineClose size={40} />
          </button>
        </div>

        <li className="p-4 uppercase text-white text-4xl font-bold">Menu:</li>

        <li className="p-4 uppercase text-white text-2xl border-b border-gray-600 hover:scale-105 hover:text-gray-600 duration-200">
          <Link to="/Upload">Upload</Link>
        </li>

        <li className="p-4 uppercase text-white text-2xl border-b border-gray-600 hover:scale-105 hover:text-gray-600 duration-200">
          <Link to="/Library">Library</Link>
        </li>

        <li className="p-4 uppercase text-white text-2xl border-b border-gray-600 hover:scale-105 hover:text-gray-600 duration-200">
          <Link to="/Outfits">Outfits</Link>
        </li>

        <li className="p-4 uppercase text-white text-2xl border-b border-gray-600 hover:scale-105 hover:text-gray-600 duration-200">
          <Link to="/">Home</Link>
        </li>
      </ul>
    </div>
  );
};

export default Library;
