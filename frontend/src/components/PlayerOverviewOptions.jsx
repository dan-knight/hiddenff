import React, {useMemo} from 'react';
import useOptions from '../hooks/useOptions';
import Accordion from './Accordion';
import ButtonGroup from './ButtonGroup';
import Searchbar from './Searchbar';

export default function PlayerOverviewOptions() {
  const optionsData = useMemo(() => ([
    { label: 'Projection Type', id: 'projType',
      default: 'average',
      buttons: [
        {label: 'Floor', value: 'floor'},
        {label: 'Average', value: 'average'},
        {label: 'Ceiling', value: 'ceiling'}
      ],
      single: true,
    },
    { label: 'Statistics Focus', id: 'statFocus',
      default: 'rush', 
      buttons: [
        {label: 'Rushing', value: 'rush'},
        {label: 'Receiving', value: 'rec'},
        {label: 'Passing', value: 'pass'},
      ]
    },
    { label: 'Statistics Format', id: 'statFormat',
      default: 'total',
      buttons: [
        {label: 'Season Total', value: 'total'},
        {label: 'Per Game', value: 'per_game'},
        {label: 'Per Attempt', value: 'per_att'}
      ], 
      single: true
    }
  ]), []);

  const [optionsState, updateOptionsState] = useOptions(optionsData);

  return (
    <Accordion label="View Options" cssClass="options" 
      topExtras={<Searchbar placeholder="Search Players" />}>
      {optionsData.map(b => (
        <ButtonGroup label={b.label} options={b.buttons} 
          selection={optionsState[b.id]} onChange={value => { updateOptionsState(value, b.id ); }}
          single={b.singleSelection} />
      ))}
    </Accordion>
  );
};