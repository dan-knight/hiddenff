import React, { useMemo } from 'react';

import PlayerTable from '../PlayerTable';

import useOptions from '../../hooks/useOptions';
import MainOptions from '../MainOptions';

export default function PlayerOverview() {
  const optionsData = useMemo(() => ({
    'pos': { 
      label: 'Positions',
      default: ['QB', 'RB', 'WR', 'TE'],
      buttons: [
        { label: 'Quarterbacks', value: 'QB' },
        { label: 'Running Backs', value: 'RB' },
        { label: 'Wide Receivers', value: 'WR' },
        { label: 'Tight Ends', value: 'TE' }
      ], 
      type: 'multi'
    },
  'gms': { 
      label: 'Games',  
      default: 'main',
      buttons: [
        { label: 'Full Slate', value: 'full' },
        { label: 'Main Slate Only', value: 'main' },
        { label: 'Primetime Slate', value: 'prime' }
      ]
    },
    'prj': { 
      label: 'Projection Type',
      default: 'average',
      buttons: [
        {label: 'Floor', value: 'floor'},
        {label: 'Average', value: 'average'},
        {label: 'Ceiling', value: 'ceiling'}
      ]
    },
    'frm': { 
      label: 'Statistics Format',
      default: 'total',
      buttons: [
        {label: 'Season Total', value: 'total'},
        // {label: 'Per Game', value: 'per_game'},
        {label: 'Per Attempt', value: 'perAtt'}
      ]
    },
    'srt': {
      default: 'name'
    },
    'sch': {
      default: ''
    }
    }), []);
  
  const selectOptions = IDs => IDs.reduce((data, id) => ({ ...data, [id]: optionsData[id] }), {});
  const mainOptions = useMemo(() => selectOptions(['pos', 'gms', 'prj', 'frm']), []);

  const [optionsState, updateOptionsState] = useOptions(optionsData, (state, { value, id }) => {
    switch (id) {
      case 'sch':
        return { ...state, sch: value, pos: optionsData.pos.default };
      case 'pos':
        return { ...state, sch: '', pos: value };
    }
  });

  function handleOptionsChange(value, key) {
    updateOptionsState(value, key);
  }

  return (
      <main>
        <MainOptions options={mainOptions} optionsState={optionsState} 
          searchbarPlaceholder="Search Players"
          onChange={handleOptionsChange} />
        <PlayerTable optionsState={optionsState} onSort={value => { handleOptionsChange(value, 'srt'); }} />
      </main>
  );
};