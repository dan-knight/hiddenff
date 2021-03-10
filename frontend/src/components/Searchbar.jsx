import React, { useEffect, useState } from 'react';
import useDebounce from '../hooks/useDebounce';

export default function Searchbar({ placeholder, stateText, onChange }) {
  const [uiText, setUIText] = useState('');
  const [debouncedText, tempText, setTempText, inProgress, clearDebounce] = useDebounce('', 250);

  useEffect(() => {
    onChange(debouncedText);
  }, [debouncedText]);

  useEffect(() => {
    clearDebounce();
    setUIText(stateText);
  }, [stateText]);

  function handleChange(e) {
    e.preventDefault();

    const newText = e.target.value;
    setUIText(newText);
    setTempText(newText);
  }

  return (
    <div className="searchbar"> 
      <input type="text" value={uiText} placeholder={placeholder} onChange={handleChange} />
    </div>
  );
};