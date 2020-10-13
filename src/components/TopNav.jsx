import React from 'react';
import { Navbar } from 'react-bootstrap';
import { Gear } from './Icons';

export default function TopNav(props) {
  function handleToggle(event) {
    event.preventDefault();
    props.onToggle();
  };

  return (
    <Navbar fixed="top" 
      variant={props.color} bg={props.color}>
      <Navbar.Collapse className="collapse w-100 order-0">
        <div onClick={handleToggle}>
          <Gear size='1.5' color='black' />
        </div>
      </Navbar.Collapse>
        <Navbar.Brand href='/'>hiddenFF</Navbar.Brand>
      <Navbar.Collapse className="collapse w-100 order-2">
          
      </Navbar.Collapse>
    </Navbar> 
  );
};