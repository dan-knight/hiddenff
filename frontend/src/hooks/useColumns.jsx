import React from 'react';
import { useMemo } from 'react';

import { columns } from '../data/columns';
import { combineArrays } from '../utility';

export default function useColumns(page, positions) {
  const pageColumns = columns[page];

  function combineColumns() {
    const s = new Set(combineArrays(...positions.map(p => pageColumns[p])));
    return combineArrays(...s);
  };

  const queryColumns = useMemo(() => combineColumns(positions), [positions]);
  const allColumns = useMemo(() => combineArrays(pageColumns.basic, queryColumns), [queryColumns]);

  return [allColumns, queryColumns];
};