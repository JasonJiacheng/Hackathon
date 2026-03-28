import React, { useState } from 'react'

const Categories = ['boots', 'hats', 'jackets', 'tops', 'trainers', 'trousers']

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
}

const Library = () => {
  const [category, setCategory] = useState('')
  const [color, setColor] = useState('')

  return (
    <div>
      <h2>Library</h2>

      <input
        type="text"
        placeholder="Search clothes"
      />

      <select
        value={category}
        onChange={(e) => setCategory(e.target.value)}
      >
        <option value=""> Type </option>
        {Categories.map(item => (
          <option key={item} value={item}>
            {item}
          </option>
        ))}
      </select>

      <select
        value={color}
        onChange={(e) => setColor(e.target.value)}
      >
        <option value="">Select colour</option>
        {Object.entries(Colours).map(([hex, name]) => (
          <option key={hex} value={hex}>
            {name}
          </option>
        ))}
      </select>

    </div>
  )
}

export default Library