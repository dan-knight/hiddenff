import React, { useEffect, useState } from 'react';

export default function useDebounce(value, delay) {
  const [tempValue, setTempValue] = useState(value);
  const [debouncedValue, setDebouncedValue] = useState(value);

  const [inProgress, setInProgress] = useState(false);
  let doLater;

  console.log(value, inProgress)

  function clear() {
    clearTimeout(doLater);
  };

  function changeValue(newValue) {
    setInProgress(true);
    setTempValue(newValue);
  }

  useEffect(() => {
    doLater = setTimeout(() => { 
      setDebouncedValue(tempValue); 
      setInProgress(false);
    }, delay);

    return () => {
      clearInterval(doLater);
    };
  }, [tempValue]);

  return [debouncedValue, tempValue, changeValue, inProgress, clear];
};