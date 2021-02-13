import React, { useState } from 'react';

export default function Searchbar(props) {
  const [text, setText] = useState('');

  function handleChange(e) {
    e.preventDefault();
    setText(e.target.value);
  }

  return (
    <div className="searchbar"> 
      <input type="text" placeholder={props.placeholder} onChange={handleChange} />
    </div>
  );
};