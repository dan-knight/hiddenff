const app = require('express')();
require('dotenv').config({ path: '../.env' });

app.get('/', (req, res) => {
  res.status(200).send('Success');
});

async function run() {
  const dbConfig = {
    host: process.env.DATABASE_HOST,
    port: parseInt(process.env.DATABASE_PORT),
    database: process.env.DATABASE_NAME,
    user: process.env.DATABASE_USER,
    password: process.env.DATABASE_PASSWORD
  };

  const db = await new require('./db').newConnection(dbConfig);

  const apiPort = process.env.API_PORT;
  app.listen(apiPort, console.log(`Listening on port ${apiPort}`));
};

run();