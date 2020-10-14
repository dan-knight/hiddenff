const axios = require('axios');

export async function getPlayers(start, sortBy, position) {
  const response = await axios({
    method: 'GET',
    url: 'http://localhost:3001/players',
    params: {
      columns: JSON.stringify(['total_rush_yd', 'total_rec_yd', 'total_pass_yd']),
      start: start,
      sortBy: sortBy,
      position: position
    }
  }).catch(error => { console.log(error); });

  return response.data;
};