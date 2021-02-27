import React from 'react';

import { CaretUp } from './Icons';

export default function Table(props) {
  return (
    <div className="data">
      <table>
        <thead>
          <tr>
            {Object.keys(props.columns).map(k => {
              const col = props.columns[k];
              return (
                <HeadCell label={col.label} colName={k}
                  sortValue={col.sortValue} sortBy={props.sortBy} unsortable={col.unsortable} 
                  onClick={props.onSort} key={k} />
              )})}
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
  const sortBy = props.colName;

  function handleClick() {
    props.onClick(sortBy);
  };

  return (
    <th key={props.colName} >
      <div onClick={props.unsortable ? null : handleClick} className={props.unsortable ? null : 'sortable'}>
        {sortBy === props.sortBy ? <CaretUp size='0.75' mb='1' /> : null} {props.label}
      </div>
    </th>
  );
};

function TableRow(props) {
  return (
    <tr>
      {Object.keys(props.columns).map(k => {
        const col = props.columns[k]
        return (
          <td key={k}>
            {col.func ? col.func(props.data) : props.data[k]}
          </td>
        )})}
    </tr>
  );
};