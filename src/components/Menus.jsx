import React from 'react';
import { Button, ButtonGroup } from 'react-bootstrap';

export function PositionMenu(props) {
  return (
    <FilterMenu
      title='Position' 
      options={[
        { value: null, label: 'All' },
        { value: 'QB', label: 'Quarterbacks' },
        { value: 'RB', label: 'Running Backs' },
        { value: 'WR', label: 'Wide Receivers' },
        { value: 'TE', label: 'Tight Ends' }
      ]} 
      value={props.value}
      onChange={props.onChange} />
  );
};

function FilterMenu(props) {
  function handleChange(event) {
    event.preventDefault();
    props.onChange(event.target.value);
  };

  return (
    <div className='py-3'>
      <h4 className='mb-3'>{props.title}</h4>
      <ButtonGroup vertical>
        {props.options.map(o => (
          <FilterButton value={o.value} active={o.value === props.value}
            key={o.value} onClick={handleChange}>{o.label || o.value}
          </FilterButton>))}
      </ButtonGroup>
    </div>
    
  )
};

function FilterButton(props) {
  return <Button onClick={props.onClick} value={props.value} variant={props.active ? 'secondary' : 'outline-secondary'}>{props.children}</Button>
}