import { getCommentTexts } from "../apis/zafApis.js";
import { detectPiiEntities as comprehendModel } from "../apis/comprehendApis.js";

const stripHtml = (text) => {
  let dom = document.createElement("div");
  dom.innerHTML = text;
  return dom.textContent || dom.innerText;
};

const concatTexts = (texts, delimiter) => {
  return texts.join(delimiter);
};

const textPreprocessor = (texts) => {
  const cleanTexts = texts.map((text) => stripHtml(text));
  return concatTexts(cleanTexts, " ");
};

const predictPiiEntities = async (text, modelName) => {
  if (modelName === "Spacy") return new Error("Spacy model is not implemented");
  else if (modelName === "Flair")
    return new Error("Flair model is not implemented");
  else if (modelName === "Comprehend") {
    const entityArray = await comprehendModel(text);
    return concatTexts(entityArray, ", ");
  }
};

const getPiiEntities = async (modelName) => {
  const comments = await getCommentTexts();
  const comment = textPreprocessor(comments);
  const entities = await predictPiiEntities(comment, modelName);
  return entities;
};

export default getPiiEntities;
