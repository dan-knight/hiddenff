import React, { useMemo } from 'react';
import useOptions from '../hooks/useOptions';
import Accordion from './Accordion';
import RadioGroup from './RadioGroup';

export default function Sidebar() {
  const optionsData = useMemo(() => (
    [
      { label: 'Positions', id: 'positions',
        default: ['QB', 'RB', 'WR', 'TE'],
        buttons: [
          { label: 'Quarterbacks', value: 'QB' },
          { label: 'Running Backs', value: 'RB' },
          { label: 'Wide Receivers', value: 'WR' },
          { label: 'Tight Ends', value: 'TE' }
      ]},
    
      { label: 'Games', id: 'slate', 
        default: 'main',
        buttons: [
          { label: 'Full Slate', value: 'full' },
          { label: 'Main Slate Only', value: 'main' },
          { label: 'Primetime Slate', value: 'prime' }
      ],
      single: true
    }]
  ), []);

  const [optionsState, updateOptionsState] = useOptions(optionsData);

  return (
    <React.Fragment>
      <div className="sidebar-buffer"></div>
      <div className="sidebar">
        {optionsData.map(m => (
          <Accordion label={m.label}>
            <RadioGroup selection={optionsState[m.id]} options={m.buttons} 
            onChange={value => { updateOptionsState(value, m.id); }} />
          </Accordion>))}
      </div>
    </React.Fragment>
  );
};

