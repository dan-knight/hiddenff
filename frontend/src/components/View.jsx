import React from 'react';
import Sidebar from './Sidebar';

export default function View({ sidebar, ...props }) {
  return (
    <React.Fragment>
      {sidebar ?? <Sidebar/>}
      <main>
        {props.children}
      </main>
      
    </React.Fragment>
  );
}