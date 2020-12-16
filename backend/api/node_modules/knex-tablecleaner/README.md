# knex-tablecleaner

Simple library for deleting all rows from a given list of DB tables.
Tables are cleaned sequentially in a given order to avoid foreign key constraint violations.

Example usage:

```js
const tableCleaner = require('knex-tablecleaner');
const knex = require('../db');

const defaultTablesToClean = [
  'orders',
  'users'
];

function cleanDb(tablesToClean = defaultTablesToClean) {
  return tableCleaner.cleanTables(knex, tablesToClean);
}

module.exports = {
  cleanDb,
};
```
