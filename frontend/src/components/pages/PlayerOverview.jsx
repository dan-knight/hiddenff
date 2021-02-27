import React, { useMemo } from 'react';

import View from '../View';
import Sidebar from '../Sidebar';
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
      ]},
      'gms': { 
        label: 'Games',  
        default: 'main',
        buttons: [
          { label: 'Full Slate', value: 'full' },
          { label: 'Main Slate Only', value: 'main' },
          { label: 'Primetime Slate', value: 'prime' }
        ],
        single: true
      },
      'prj': { 
        label: 'Projection Type',
        default: 'average',
        buttons: [
          {label: 'Floor', value: 'floor'},
          {label: 'Average', value: 'average'},
          {label: 'Ceiling', value: 'ceiling'}
        ],
        single: true,
      },
      'fcs': { 
        label: 'Statistics Focus',
        default: 'rush', 
        buttons: [
          {label: 'Rushing', value: 'rush'},
          {label: 'Receiving', value: 'rec'},
          {label: 'Passing', value: 'pass'},
      ]},
      'frm': { 
        label: 'Statistics Format',
        default: 'total',
        buttons: [
          {label: 'Season Total', value: 'total'},
          // {label: 'Per Game', value: 'per_game'},
          {label: 'Per Attempt', value: 'perAtt'}
        ], 
        single: true
      },
      'srt': {
        default: 'name',
        single: true
      }
    }), []);
  
  const selectOptions = IDs => IDs.reduce((data, id) => ({ ...data, [id]: optionsData[id] }), {});
  const sidebarOptions = useMemo(() => selectOptions(['pos', 'gms']), []);
  const mainOptions = useMemo(() => selectOptions(['prj', 'fcs', 'frm']), []);

  const [optionsState, updateOptionsState] = useOptions(optionsData);

  return (
      <View sidebar={<Sidebar options={sidebarOptions} optionSelections={optionsState} onChange={updateOptionsState} />}>
        <MainOptions options={mainOptions} optionsState={optionsState} 
          searchbarPlaceholder="Search Players"
          onChange={updateOptionsState} />
        <PlayerTable optionsState={optionsState} onSort={value => { updateOptionsState(value, 'srt'); }} />
      </View>
  );
};