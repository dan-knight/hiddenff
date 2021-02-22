import React from 'react';

import { isSelected } from '../utility';

export default function ButtonGroup({ label, options, selection, single, onChange }) {
  return (
    <div className='button-group'>
      <label>{label}</label>
      {options.map(b => (
        <Button value={b.value} label={b.label} 
        isSelected={isSelected(b.value, selection, single)} onToggle={onChange} />
      ))}
    </div>
  );
};

function Button({ label, value, isSelected, onToggle }) {
  return (
    <button name={value} className={isSelected ? 'selected' : ''} onClick={() => { onToggle(value); }}>
      <span>{label}</span>
    </button>
  );
}