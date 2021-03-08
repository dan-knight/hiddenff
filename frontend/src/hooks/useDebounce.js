import React, { useEffect, useState } from 'react';

export default function useDebounce(value, delay) {
  const [tempValue, setTempValue] = useState(value);
  const [debouncedValue, setDebouncedValue] = useState(value);

  const [inProgress, setInProgress] = useState(false);

  useEffect(() => {
    setInProgress(true);

    const doLater = setTimeout(() => { 
      setDebouncedValue(tempValue); 
      setInProgress(false);
    }, delay);

    return () => {
      clearInterval(doLater);
    };
  }, [tempValue]);

  return [debouncedValue, tempValue, setTempValue, inProgress];
};