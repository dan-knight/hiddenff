import React, { useEffect } from 'react';
import useDebounce from '../hooks/useDebounce';

export default function Searchbar({ placeholder, onChange }) {
  const [apiText, uiText, setText] = useDebounce('', 250);

  useEffect(() => {
    onChange(apiText);
  }, [apiText]);

  function handleChange(e) {
    e.preventDefault();
    setText(e.target.value);
  }

  return (
    <div className="searchbar"> 
      <input type="text" value={uiText} placeholder={placeholder} onChange={handleChange} />
    </div>
  );
};