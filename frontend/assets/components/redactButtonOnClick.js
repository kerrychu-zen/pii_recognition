import redact from "./redact.js";

const onClickRedact = () => {
  const text = document.querySelector("#pii-entities").innerText;
  redact(text);
};

document.querySelector("#redact").addEventListener("click", onClickRedact);
