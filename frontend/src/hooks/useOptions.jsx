import { useMemo, useReducer } from 'react';

export default function useOptions(optionsData) {
  const selectionTypes = useMemo(() => optionsData.reduce((types, o) => ({ ...types, [o.id]: o.single }), {}), [optionsData]);
  const initialOptionValues = () => optionsData.reduce((state, o) => (
    { ...state, [o.id]: o.single ? o.default : (Array.isArray(o.default) ? [...o.default] : [o.default]) }), {});
  
  const updatedValue = (prevSelected, value, single ) => {
    return single ? value : updateMultipleSelection(prevSelected, value)
  };

  function updateMultipleSelection(prevSelected, value) {
    return prevSelected.includes(value) ? prevSelected.filter(o => o !== value) : [ ...prevSelected, value ]
  }

  const reducer = (state, { id, value }) => (
    { ...state, [id]: updatedValue(state[id], value, selectionTypes[id]) });

  const [state, dispatch] = useReducer(reducer, initialOptionValues());
  return [state, (value, id) => { dispatch({ value, id }); }]
};