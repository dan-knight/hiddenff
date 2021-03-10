import { useMemo, useReducer } from 'react';

export default function useOptions(optionsData, specialCases=(() => undefined)) {
  const initialOptionValues = useMemo(() => (
    Object.keys(optionsData).reduce((state, k) => {
      const option = optionsData[k];

      return { ...state, [k]: option.single ? 
        option.default : (Array.isArray(option.default) ? [...option.default] : [option.default]) 
      };
    }, {})
  ), []);

  const reducer = (state, { value, id }) => {
    return specialCases(state, { value, id }) ?? { ...state, [id]: value };
  };

  const [state, dispatch] = useReducer(reducer, initialOptionValues);
  return [state, (value, id) => { dispatch({ value, id }); }]
};