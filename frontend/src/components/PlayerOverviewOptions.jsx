import React from 'react';
import Accordion from './Accordion';
import ButtonGroup from './ButtonGroup';
import Searchbar from './Searchbar';

export default function PlayerOverviewOptions() {
  return (
    <Accordion label="View Options" collapseID="options" 
      cssClass="options" topExtras={<Searchbar placeholder="Search Players" />}
      >
      {buttonData.map(b => <ButtonGroup label={b.label} buttons={b.buttons} />)}
    </Accordion>
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