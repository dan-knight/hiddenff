import { useMemo, useReducer } from 'react';

export default function useOptions(optionsData) {
  const selectionTypes = useMemo(() => Object.keys(optionsData).reduce(
    (types, id) => ({ ...types, [id]: optionsData[id].single })
  , {}), [optionsData]);
  
  const initialOptionValues = useMemo(() => (
    Object.keys(optionsData).reduce((state, k) => {
      const option = optionsData[k];

      return { ...state, [k]: option.single ? 
        option.default : (Array.isArray(option.default) ? [...option.default] : [option.default]) 
      };
    }, {})
  ), []);

  const updatedValue = (prevSelected, value, single ) => {
    return single ? value : updateMultipleSelection(prevSelected, value)
  };

  function updateMultipleSelection(prevSelected, value) {
    return prevSelected.includes(value) ? prevSelected.filter(o => o !== value) : [ ...prevSelected, value ]
  }

  const reducer = (state, { id, value }) => (
    { ...state, [id]: updatedValue(state[id], value, selectionTypes[id]) });

  const [state, dispatch] = useReducer(reducer, initialOptionValues);
  return [state, (value, id) => { dispatch({ value, id }); }]
};