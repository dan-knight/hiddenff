export function capitalizeSentence(sentence) {
  const capitalize = word => word.charAt(0).toUpperCase() + word.slice(1);
  const capitalizedWords = sentence.split(' ').map(w => capitalize(w));
  return capitalizedWords.join(' ');
};