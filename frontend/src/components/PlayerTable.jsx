import React, { useEffect } from 'react';

import Table from './Table';

import useAxios from '../hooks/useAxios'
import useDataStorage from '../hooks/useDataStorage';

import { playerColumns } from  '../data/columns';

export default function PlayerTable({ optionsState, onSort }) {
  const [loading, error, request] = useAxios();
  const [playerData, updateData, replaceData] = useDataStorage();

  useEffect(function() {
    replacePlayerData();
  }, [optionsState]);

  async function getPlayerData(start=0) {
    const newData = await request({ 
      url: 'http://localhost:3001/players',
      // url: 'https://api.hiddenff.com/players',
      params: {
        pos: JSON.stringify(optionsState.pos),
        srt: optionsState.srt,
        frm: optionsState.frm,
        start: start
      }
    })

    return newData;
  };

  async function replacePlayerData() {
    const response = await getPlayerData();
    replaceData(response.data);
    
    if (response.sortedBy !== optionsState.srt) {
      onSort(response.sortedBy);
    };
  };

  async function updatePlayerData() {
    updateData(await getPlayerData(playerData.length));
  };

  const columns = (() => { 
    const columnData = playerColumns();

    const getDataColumns = () => {
      const allColumns = Object.keys(playerData[0]);
      const columnNames = allColumns.filter(col => !['id'].includes(col));
      return columnNames.reduce((columns, n) => ({ ...columns, [n]: columnData[n]}), {});
    };

    return playerData.length > 0 ? getDataColumns() : {}; 
  })();

  return <Table data={playerData} columns={columns} sortBy={optionsState.srt} loading={loading} onSort={onSort} />; 
}