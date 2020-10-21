const axios = require('axios');

const dbURL = `http://localhost:${process.env.API_PORT}`;

export async function getPlayers(start, sortBy, position) {
  const response = await axios({
    method: 'GET',
    url: `${dbURL}/players`,
    params: {
      columns: JSON.stringify(['total_rush_yd', 'total_rec_yd', 'total_pass_yd']),
      start: start,
      sortBy: sortBy,
      position: position
    }
  }).catch(error => { console.log(error); });

  return response ? response.data : [];
};