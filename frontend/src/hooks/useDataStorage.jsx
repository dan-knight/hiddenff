import React, { useState } from 'react';

export default function useDataStorage() {
  const [data, setData] = useState([]);

  function update(newData) {
    setData([...data, ...newData]);
  };

  function replace(newData) {
    setData(newData);
  };

  return [data, update, replace];
};