const utility = require ('./utility');

const knex = require('knex');
const knexUtils = require('knex-utils');
const heartbeatChecker = require('knex-utils').heartbeatChecker;

class Database {
  constructor(config) {
    this.dbInstance = knex({
      client: 'mysql2',
      connection: config
    });
  };

  async isConnected() {
    const response = await heartbeatChecker.checkHeartbeat(this.dbInstance, heartbeatChecker.HEARTBEAT_QUERIES.MYSQL);
    return response['isOk'];
  };

  async getPlayers(positions, focus, format, orderBy, start) {
    const columns = (() => {
      const statColumns = focus.reduce((columns, foc) => columns.concat(playerColumns[foc][format]), []);
      return ['id', knex.raw('CONCAT(first, " ", last) as name'), 'position', 'team_id as team'].concat(statColumns);
    })();

    console.log(columns)
    const query = await this.dbInstance.select(columns).from('players')
      .orderBy(orderBy, orderBy === 'name' ? 'asc' : 'desc')
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
      .limit(20).offset(start);

    return query;
  };
};

const playerColumns = {
  pass: {
    total: ['total_pass_att', 'total_pass_cmp', 'total_pass_yd', 'total_pass_td'],
    perAtt: ['total_pass_yd_per_cmp']
  },
  rush: {
    total: ['total_rush_att', 'total_rush_yd', 'total_rush_td'],
    perAtt: ['total_rush_yd_per_att']
  },
  rec: {
    total: ['total_tgt', 'total_rec', 'total_rec_yd', 'total_rec_td'],
    perAtt: ['total_rec_yd_per_rec']
  }
};

exports.newConnection = async config => {
  const db = new Database(config);
  if (await db.isConnected()) {
    return db;
  } else throw new Error();
};