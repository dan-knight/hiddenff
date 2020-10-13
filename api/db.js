const knexUtils = require('knex-utils');

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

  async getPlayers(orderBy, startNumber, position) {
    const query = await this.dbInstance.select(['first', 'last', 'position', 'team_id'])
      .from('players').orderBy(orderBy).where(position ? { position: position } : {})
      .limit(20).offset(startNumber);
    return query;
  };
};

exports.newConnection = async config => {
  const db = new Database(config);
  if (await db.isConnected()) {
    return db;
  } else throw new Error();
};