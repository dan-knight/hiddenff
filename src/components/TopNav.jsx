import React from 'react';
import { Nav, Navbar } from 'react-bootstrap';

export default function TopNav(props) {
  return (
    <Navbar fixed="top" 
      variant={props.color} bg={props.color}>
      <Navbar.Collapse className="collapse w-100 order-0">
        
      </Navbar.Collapse>
        <Navbar.Brand href='/'>hiddenFF</Navbar.Brand>
      <Navbar.Collapse className="collapse w-100 order-2">
          
      </Navbar.Collapse>
    </Navbar> 
  );
};