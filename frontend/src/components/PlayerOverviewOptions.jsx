import React from 'react';
import ButtonGroup from './ButtonGroup';
import Searchbar from './Searchbar';

export default function PlayerOverviewOptions(props) {
  return (
    <div className="options">
      <div className="top">
        <span className="toggle">
          View Options
        </span>
        <Searchbar placeholder="Search Players" />
      </div>
      <div className="content" id="options-content">
        {buttonData.map(b => <ButtonGroup label={b.label} buttons={b.buttons} />)}
      </div>
    </div>
  );
};

const buttonData = [
  {label: 'Projection Type', buttons: [
    {label: 'Floor', value: 'floor'},
    {label: 'Average', value: 'average'},
    {label: 'Ceiling', value: 'ceiling'}
  ]},
  {label: 'Statistics Focus', buttons: [
    {label: 'Rushing', value: 'rush'},
    {label: 'Receiving', value: 'rec'},
    {label: 'Passing', value: 'pass'},
  ]},
  {label: 'Statistics Format', buttons: [
    {label: 'Season Total', value: 'total'},
    {label: 'Per Game', value: 'per_game'},
    {label: 'Per Attempt', value: 'per_att'}
  ]}
];