import React from 'react';
import { useEffect, useMemo } from 'react';

import useAxios from '../hooks/useAxios'
import useDataStorage from '../hooks/useDataStorage';
import Table from './Table';

import useColumns from '../hooks/useColumns';

export default function PlayerTable(props) {
  const [loading, error, request] = useAxios();
  const [playerData, updateData, replaceData] = useDataStorage();

  const [allColumns, viewColumns] = useColumns('playerOverview', props.positions);
  const queryColumns = useMemo(() => JSON.stringify(viewColumns.map(c => c.name)), [viewColumns]);

  useEffect(function() {
    replacePlayerData();
  }, [props.positions, props.sortBy]);

  async function getPlayerData(start=0) {
    const newData = await request({ 
      // url: 'http://localhost:3001/players',
      url: 'https://api.hiddenff.com/players',
      params: {
        columns: queryColumns,
        positions: JSON.stringify(props.positions),
        sortBy: props.sortBy,
        start: start
      }
    })

    return newData;
  };

  async function replacePlayerData() {
    replaceData(await getPlayerData())
  };

  async function updatePlayerData() {
    updateData(await getPlayerData(playerData.length));
  };

  return (
    <main>
      <Table data={playerData} columns={allColumns} sortBy={props.sortBy} onSort={props.onSort} />
    </main>
  ); 
}