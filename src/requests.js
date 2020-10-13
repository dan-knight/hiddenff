const axios = require('axios');

export async function getPlayers(start, orderBy, position) {
  const response = await axios({
    method: 'GET',
    url: 'http://localhost:3001/players',
    params: {
      start: start,
      orderBy: orderBy,
      position: position
    }
  }).catch(error => { console.log(error); });

  return response.data;
};