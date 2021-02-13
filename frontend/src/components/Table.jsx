import React from 'react';

import { CaretUp } from './Icons';

export default function Table(props) {
  return (
    <div className="data">
      <table>
        <thead>
          <tr>
            {props.columns.map(col => (
              <HeadCell label={col.label} colName={col.name}
                sortValue={col.sortValue} sortBy={props.sortBy} sortable={col.sortable} 
                onClick={props.onSort} key={col.name} />))}
          </tr> 
        </thead>
        <tbody>
          {props.data.map(d => <TableRow key={d.id} data={d} columns={props.columns} />)}
        </tbody>
      </table>
    </div>
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
      {props.columns.map(col => <td key={col.name}>{col.func ? col.func(props.data) : Number(props.data[col.name]).toFixed(1)}</td>)}
    </tr>
  );
};