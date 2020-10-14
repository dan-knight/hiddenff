require('dotenv').config({ path: '../.env' });
const utility = require('./utility');

async function run() {
  const dbConfig = {
    host: process.env.DATABASE_HOST,
    port: parseInt(process.env.DATABASE_PORT),
    database: process.env.DATABASE_NAME,
    user: process.env.DATABASE_USER,
    password: process.env.DATABASE_PASSWORD
  };

  const db = await new require('./db').newConnection(dbConfig);


  const app = require('express')();
  app.use(require('cors')());

  app.get('/players', async (req, res) => {
    const players = await db.getPlayers(req.query.columns, req.query.sortBy, req.query.start * 20, req.query.position);
    // players.forEach(p => utility.renameKey(p, 'team_id', 'team'));

    res.status(200).json(players);
  });


  const apiPort = process.env.API_PORT;
  app.listen(apiPort, console.log(`Listening on port ${apiPort}`));
};

run();