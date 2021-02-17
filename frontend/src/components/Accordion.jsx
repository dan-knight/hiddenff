import React from 'react';

export default function Accordion({ label, collapseID, ...props }) {
  function handleToggle() {
    alert('click');
  };

  return (
    <div>
      <div className='top'>
        <Toggle label={label} onToggle={handleToggle} />
      </div>
      <div className="content" id={collapseID}>
        {props.children}
      </div>
    </div>
  );
};

function Toggle({ label, onToggle }) {
  return (
    <div className="toggle" onClick={onToggle}>
      <h5>{label}</h5>
    </div>
  );
}