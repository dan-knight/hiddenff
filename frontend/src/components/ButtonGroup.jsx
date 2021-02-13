import React, { useState } from 'react';

export default function ButtonGroup(props) {
  const [value, setValue] = useState(props.default);

  function handleChange(e) {
    e.preventDefault();
    setValue(e.target.value);
  }

  return (
    <div className='button-group'>
      <label>{props.label}</label>
      {props.buttons.map(b => <Button label={b.label} className={value === b.value ? 'active' : ''} />)}
    </div>
  );
};

function Button(props) {
  return (
    <button>
      <span>{props.label}</span>
    </button>
  );
}