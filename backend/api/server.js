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
    const positions = req.query.pos ? utility.parseQueryJSON(req, 'pos') : ['QB', 'RB', 'WR', 'TE'];
    const focus = req.query.fcs ? utility.parseQueryJSON(req, 'fcs') : ['pass', 'rush', 'rec'];
    const format = req.query.frm ?? 'total';
    const sortBy = req.query.srt ?? 'last';

    const start = (() => {
      const defaultStart = 0;

      if (req.query.start) {
        const parsed = parseInt(req.query.start);
        return isNaN(parsed) ? defaultStart : parsed;
      } else return defaultStart;  
    })();
    
    try {
      const players = await db.getPlayers(positions, focus, format, sortBy, start);
      res.status(200).json(players);
    } catch (error) {
      res.status(500).send();
    }
  });


  const apiPort = process.env.API_PORT;
  app.listen(apiPort, console.log(`Listening on port ${apiPort}`));
};

run();