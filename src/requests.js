const axios = require('axios');

export async function getPlayers(start=0, orderBy='last', position=null) {
  const response = await axios({
    method: 'GET',
    url: 'http://localhost:3001/players',
    params: {
      start: start,
      orderBy: orderBy
    }
  }).catch(error => { console.log(error); });

  return response.data;
};