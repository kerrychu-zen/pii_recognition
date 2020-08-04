import getPiiEntities from "./piiDetectButton.js";

// must take no argument
const onClickDetect = async () => {
  const modelName = document.querySelector("#model-name").value;
  const piiEntities = await getPiiEntities(modelName);
  document.querySelector("#pii-entities").innerHTML = piiEntities;
};

document.querySelector("#detect").addEventListener("click", onClickDetect);
