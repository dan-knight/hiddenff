import React from 'react';
import $ from 'jquery';
import Divider from './Divider';

export default function Accordion({ label, collapseID, ...props }) {
  function handleToggle() {
    $(`#${collapseID}`).slideToggle();
  };

  return (
    <div>
      <div className='top'>
        <Toggle label={label} onToggle={handleToggle} />
      </div>
      <div className="content" id={collapseID}>
        {props.children}
      </div>
      <Divider />
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