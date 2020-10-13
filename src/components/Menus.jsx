import React from 'react';
import { Button, ButtonGroup } from 'react-bootstrap';

export function PositionMenu(props) {
  return (
    <FilterMenu
      title='Position' 
      options={[
        { value: '', label: 'All' },
        { value: 'QB'},
        { value: 'RB'},
        { value: 'WR'},
        { value: 'TE'}
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
    <div>
      <h4>{props.title}</h4>
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
  return <Button onClick={props.onClick} value={props.value} variant={props.active ? 'primary' : 'outline-primary'}>{props.children}</Button>
}