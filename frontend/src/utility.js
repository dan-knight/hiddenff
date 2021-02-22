export function capitalizeSentence(sentence) {
  const capitalize = word => word.charAt(0).toUpperCase() + word.slice(1);
  const capitalizedWords = sentence.split(' ').map(w => capitalize(w));
  return capitalizedWords.join(' ');
};

export function combineArrays(...arrays) {
  return [].concat(...arrays);
};

export const isSelected = (value, selection, single) => {
  return single ? value === selection : selection.includes(value)
};