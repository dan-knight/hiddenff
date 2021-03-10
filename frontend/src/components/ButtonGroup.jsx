import React, { useCallback, useEffect, useState } from 'react';
import useDebounce from '../hooks/useDebounce';

import { isSelected } from '../utility';

export default function ButtonGroup({ label, options, selection, type, onChange }) {
  return (
    <div className='button-group'>
      <label>{label}</label>
      <ButtonFactory options={options} selection={selection} type={type} onChange={onChange} />
    </div>
  );
};

function ButtonFactory({ options, selection, type, onChange }) {
  return useCallback(selectionState => (
    type === 'multi' ? (
      <MultiButtonGroup options={options} stateSelection={selectionState} onChange={onChange} />
    ) : (
      <SingleButtonGroup options={options} selection={selectionState} onChange={onChange} />
    )
  ), [type])(selection);
};

function SingleButtonGroup({ options, selection, onChange }) {
  return (
    <React.Fragment>
      {options.map(b => (
        <Button value={b.value} label={b.label} 
        isSelected={isSelected(b.value, selection)} onChange={onChange} />
      ))}
    </React.Fragment>
  );
};

function MultiButtonGroup({ options, stateSelection, onChange }) {
  const [uiSelection, setUISelection] = useState(stateSelection);
  const [debouncedSelection, tempSelection, setSelection, debounceInProgress, clearDebounce] = useDebounce(stateSelection, 700);

  function handleChange(value) {
    function removeValue() {
      return uiSelection.length === 1 ? uiSelection : uiSelection.filter(s => s !== value);
    };

    if (debounceInProgress) {
      setSelection(uiSelection.includes(value) ? removeValue() : [...uiSelection, value]);
    } else setSelection([value]);    
  };

  useEffect(() => {
    clearDebounce();
    setUISelection(stateSelection);
  }, [stateSelection]);

  useEffect(() => { 
    onChange(debouncedSelection);
  }, [debouncedSelection]);

  useEffect(() => {
    setUISelection(tempSelection);
  }, [tempSelection])

  return (
    <React.Fragment>
      {options.map(b => (
        <Button value={b.value} label={b.label} 
        isSelected={isSelected(b.value, uiSelection)} onChange={handleChange} />
      ))}
    </React.Fragment>
  );
}

function Button({ label, value, isSelected, onChange }) {
  return (
    <button name={value} className={isSelected ? 'selected' : ''} onClick={() => { onChange(value); }}>
      <span>{label}</span>
    </button>
  );
}