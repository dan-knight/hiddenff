import React, { useState } from 'react';

export default function RadioGroup({ options }) {
  const [selected, setSelected] = useState(options.map(o => o.value));

  function handleChange(name) {
    setSelected(selected.includes(name) ? selected.filter(o => o !== name) : [ ...selected, name ]);
  }

  return (
    <div className="radio-group">
      {options.map(o => (
        <label name={o.value} onClick={() => handleChange(o.value)}>
          <div className={selected.includes(o.value) ? 'checked' : ''} />
          <span>{o.label}</span>
        </label>
      ))}
    </div>
  );
}