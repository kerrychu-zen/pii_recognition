const resetCallout = () => {
  const emptyString = "";
  document.querySelector("#pii-entities").innerHTML = emptyString;
};
document.querySelector("#reset").addEventListener("click", resetCallout);
