const stripHtml = (text) => {
  let dom = document.createElement("div");
  dom.innerHTML = text;
  return dom.textContent || dom.innerText;
};

const concatStrings = (strings, delimiter) => {
  return strings.join(delimiter);
};

const removeWhitespace = (string) => {
  return string.trim();
};

const handle = (promise) => {
  return promise
    .then((data) => [data, undefined])
    .catch((error) => Promise.resolve([undefined, error]));
};

export { stripHtml, concatStrings, removeWhitespace, handle };
