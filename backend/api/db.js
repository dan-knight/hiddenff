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

  async getPlayers(columns, orderBy, startNumber, positions) {
    const getColumns = () => ['id', 'first', 'last', 'position', 'team_id'].concat(columns);

    const query = await this.dbInstance.select(getColumns())
      .from('players').orderBy(orderBy, orderBy === 'last' ? 'asc' : 'desc')
      .where(builder => {
        const length = positions.length;

        if (length < 3) {
          builder.whereIn('position', positions);
        } else if (length > 3) {
          builder.whereNotIn('position', []);
        } else {
          builder.whereNotIn('position', ['QB', 'RB', 'WR', 'TE'].filter(p => !positions.includes(p)));
        };
      })
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