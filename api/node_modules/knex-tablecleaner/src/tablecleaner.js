const async = require("async");

function cleanTables(knex, tableNames, verboseLog = false) {
  return new Promise((resolve, reject) => {
    let commands = [];
    for (tableName of tableNames) {
      commands.push(_makeCleanTableCommand(knex, tableName, verboseLog));
    }

    async.series(commands, (err, results) => {
      if (err) {
        reject(err);
      } else {
        resolve(results);
      }
    });
  });
}

function _makeCleanTableCommand(knex, tableName, verboseLog) {
  return function(callback) {
    if (verboseLog) {
      console.log("Deleting all rows from table " + tableName);
    }
    return knex(tableName)
      .del()
      .then(function(result) {
        if (verboseLog) {
          console.log("Done deleting. Deleted: " + result);
        }
        callback(null, result);
      })
      .catch(err => {
        callback(err);
      });
  };
}

module.exports = {
  cleanTables
};
