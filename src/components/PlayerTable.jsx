import React from 'react';
import { useEffect } from 'react';

import useAxios from '../hooks/useAxios'
import useDataStorage from '../hooks/useDataStorage';
import Table from './Table';

import {columns} from '../data/columns';

export default function PlayerTable(props) {
  const [loading, error, request] = useAxios();
  const [playerData, updateData, replaceData] = useDataStorage();

  useEffect(function() {
    replacePlayerData();
  }, [props.position, props.sortBy]);

  async function getPlayerData(start=0) {
    const newData = await request({ 
      url: 'http://localhost:3001/players',
      params: {
        columns: JSON.stringify(['total_rush_yd', 'total_rec_yd', 'total_pass_yd']),
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
      {/* <button onClick={updatePlayerData}>Update</button>
      {loading ? 'Loading...' : JSON.stringify(playerData)} */}
      <Table data={playerData} columns={columns} sortBy={props.sortBy} onSort={props.onSort} />
    </div>
  ); 
}