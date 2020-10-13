require('dotenv');
const heartbeatChecker = require('knex-utils').heartbeatChecker;

class Database {
  constructor(config) {
    this.dbInstance = require('knex')({
      client: 'mysql2',
      connection: config
    });
  };

  async isConnected() {
    const response = await heartbeatChecker.checkHeartbeat(this.dbInstance, heartbeatChecker.HEARTBEAT_QUERIES.MYSQL);
    return response['isOk'];
  };
};

exports.newConnection = async config => {
  const db = new Database(config);
  if (await db.isConnected()) {
    return db;
  } else throw new Error();
};