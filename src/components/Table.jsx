import React from 'react';

import { Table as BootstrapTable } from 'react-bootstrap';
import { capitalizeWords } from '../utility';

export default function Table(props) {
  return (
    <BootstrapTable striped bordered hover>
      <thead>
        <tr>
        {props.columns.map((col) => <th key={col.label}>{capitalizeWords(col.label)}</th>)}
        </tr> 
      </thead>
      <tbody>
        {props.data.map((d, i) => <TableRow key={i} data={d} columns={props.columns} />)}
      </tbody>
    </BootstrapTable>
  );
};

function TableRow(props) {
  return (
    <tr>
      {props.columns.map(col => <td key={col.label}>{col.func(props.data)}</td>)}
    </tr>
  );
};