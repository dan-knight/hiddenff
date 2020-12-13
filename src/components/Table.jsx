import React from 'react';

import { Table as BootstrapTable } from 'react-bootstrap';
import { capitalizeSentence } from '../utility';
import { CaretUp } from './Icons';

export default function Table(props) {
  return (
    <BootstrapTable striped bordered hover>
      <thead>
        <tr>
          {props.columns.map(col => (
            <HeadCell label={col.label} colName={col.name}
              sortValue={col.sortValue} sortBy={props.sortBy} sortable={col.sortable} onClick={props.onSort}/>))}
        </tr> 
      </thead>
      <tbody>
        {props.data.map((d, i) => <TableRow key={i} data={d} columns={props.columns} />)}
      </tbody>
    </BootstrapTable>
  );
};

function HeadCell(props) {
  const sortBy = props.sortValue || props.colName;

  function handleClick() {
    props.onClick(sortBy);
  };

  return (
    <th key={props.colName} >
      <div onClick={props.sortable ? handleClick : null} className={props.sortable ? 'sortable' : null}>
        {sortBy === props.sortBy ? <CaretUp size='0.75' mb='1' /> : null} {props.label}
      </div>
    </th>
  );
};

function TableRow(props) {
  return (
    <tr>
      {props.columns.map(col => <td key={col.label}>{col.func ? col.func(props.data) : props.data[col.name]}</td>)}
    </tr>
  );
};