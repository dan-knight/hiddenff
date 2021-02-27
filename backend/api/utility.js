exports.renameKey = (obj, oldKey, newKey) => {
  obj[newKey] = obj[oldKey];
  delete obj[oldKey];
};

exports.parseQueryJSON = (req, key) => {
  try {
    return JSON.parse(req.query[key]);
  } catch {
    return [];
  };
};

exports.checkArray = data => {
  return Array.isArray(data) ? data : [data];
}