import React from 'react';

import { isSelected } from '../utility';

export default function RadioGroup({ options, selection, single, onChange }) {
  return (
    <div className="radio-group">
      {options.map(o => (
        <Radio value={o.value} label={o.label} 
        selected={isSelected(o.value, selection, single)} onChange={onChange} />
      ))}
    </div>
  );
};

function Radio({ label, value, selected, onChange }) {
  return (
    <label onClick={() => onChange(value)}>
      <div className={selected ? 'checked' : ''} />
      <span>{label}</span>
    </label>
  )
}