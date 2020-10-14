import React from 'react';

import { Table as BootstrapTable } from 'react-bootstrap';
import { capitalizeSentence } from '../utility';

export default function Table(props) {
  return (
    <BootstrapTable striped bordered hover>
      <thead>
        <tr>
          {props.columns.map(col => (
            <HeadCell label={col.label || capitalizeSentence(col.name)} colName={col.name}
              sortValue={col.sortValue} sortable={col.sortable} onClick={props.onSort}/>))}
        </tr> 
      </thead>
      <tbody>
        {props.data.map((d, i) => <TableRow key={i} data={d} columns={props.columns} />)}
      </tbody>
    </BootstrapTable>
  );
};

function HeadCell(props) {
  function handleClick() {
    props.onClick(props.sortValue || props.colName);
  };

  return (
    <th key={props.colName} >
      <div onClick={props.sortable ? handleClick : null}>
        {props.label}
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