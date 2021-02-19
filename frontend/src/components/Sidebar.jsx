import React from 'react';
import Accordion from './Accordion';
import RadioGroup from './RadioGroup';

export default function Sidebar(props) {
  return (
    <React.Fragment>
      <div className="sidebar-buffer"></div>
      <div className="sidebar">
        {menus.map(m => (
          <Accordion label={m.label}>
            <RadioGroup options={m.options} />
          </Accordion>))}
      </div>
    </React.Fragment>
  );
};

const menus = [
  { label: 'Positions', id: 'positions',
    options: [
      { label: 'Quarterbacks', value: 'QB' },
      { label: 'Running Backs', value: 'RB' },
      { label: 'Wide Receivers', value: 'WR' },
      { label: 'Tight Ends', value: 'TE' }
  ]},

  { label: 'Games', id: 'games', 
    options: [
      { label: 'Full Slate', value: 'full' },
      { label: 'Main Slate Only', value: 'main' },
      { label: 'Primetime Slate', value: 'prime' }
  ]}
];