import React, { useCallback } from 'react';

export default function useBottomScroll(doAtBottom) {
  const isAtBottom = useCallback(event => {
    const element = event.target;
    return element.scrollHeight - element.scrollTop === element.clientHeight;
  }, []);

  return function(event) {
    if (isAtBottom(event)) {
      doAtBottom();
    };
  };
};