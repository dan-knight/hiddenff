export function capitalizeWords(sentence) {
  const capitalize = word => word.charAt(0).toUpperCase() + word.slice(1);
  return sentence.split(' ').map(w => capitalize(w));
};