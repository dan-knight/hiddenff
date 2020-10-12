import React from 'react';

import { Table as BootstrapTable } from 'react-bootstrap';
import { capitalizeWords } from '../utility';

export default function Table(props) {
  return (
    <BootstrapTable striped bordered hover>
      <thead>
        {props.columns.map((col) => <th key={col}>{capitalizeWords(col)}</th>)}
      </thead>
      <tbody>
        {props.data.map(d => <TableRow data={d} columns={props.columns} />)}
      </tbody>
    </BootstrapTable>
  );
};

function TableRow(props) {
  return (
    <tr>
      {props.columns.map(col => <td key={col}>{props.data[col]}</td>)}
    </tr>
  );
};