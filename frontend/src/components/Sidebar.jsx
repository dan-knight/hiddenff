import React, { useMemo } from 'react';
import useOptions from '../hooks/useOptions';
import Accordion from './Accordion';
import RadioGroup from './RadioGroup';

export default function Sidebar({ options={}, optionSelections, onChange }) {
  

  return (
    <React.Fragment>
      <div className="sidebar-buffer"></div>
      <div className="sidebar">
        {Object.keys(options).map(k => {
          const option = options[k];
          return (
            <Accordion label={option.label}>
              <RadioGroup selection={optionSelections[k]} options={option.buttons} 
              onChange={value => { onChange(value, k); }} />
            </Accordion>
          )})}
      </div>
    </React.Fragment>
  );
};

