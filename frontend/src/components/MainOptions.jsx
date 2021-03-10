import React from 'react';
import Accordion from './Accordion';
import ButtonGroup from './ButtonGroup';
import Searchbar from './Searchbar';



export default function MainOptions({ options, optionsState, searchbarPlaceholder, onChange }) {
  return (
    <Accordion label="View Options" cssClass="options" 
      topExtras={
        <Searchbar placeholder={searchbarPlaceholder} stateText={optionsState.sch} onChange={value => { onChange(value, 'sch'); }}/>
      }>
      {Object.keys(options).map(k => {
        const option = options[k];

        return (
        <ButtonGroup label={option.label} options={option.buttons} type={option.type}
          selection={optionsState[k]} onChange={value => { onChange(value, k ); }} />
        );
      })}
    </Accordion>
  );
}
