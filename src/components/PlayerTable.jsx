import React from 'react';
import { useEffect, useMemo } from 'react';

import useAxios from '../hooks/useAxios'
import useDataStorage from '../hooks/useDataStorage';
import Table from './Table';

import useColumns from '../hooks/useColumns';

export default function PlayerTable(props) {
  const [loading, error, request] = useAxios();
  const [playerData, updateData, replaceData] = useDataStorage();

  const [allColumns, viewColumns] = useColumns('playerOverview', props.position);
  const queryColumns = useMemo(() => JSON.stringify(viewColumns.map(c => c.name)), [viewColumns]);

  useEffect(function() {
    replacePlayerData();
  }, [props.position, props.sortBy]);

  async function getPlayerData(start=0) {
    const newData = await request({ 
      url: 'http://localhost:3001/players',
      params: {
        columns: queryColumns,
        position: props.position,
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
    <div>
      <Table data={playerData} columns={allColumns} sortBy={props.sortBy} onSort={props.onSort} />
    </div>
  ); 
}