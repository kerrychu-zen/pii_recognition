import { getCommentTexts } from "../apis/zafApis.js";
import { detectPiiEntities as comprehendModel } from "../apis/comprehendApis.js";
import { stripHtml, concatStrings } from "../utils.js";

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
    return concatStrings(entityArray, ", ");
  }
};

const getPiiEntities = async (modelName) => {
  const comments = await getCommentTexts();
  const comment = textPreprocessor(comments);
  const entities = await predictPiiEntities(comment, modelName);
  return entities;
};

export default getPiiEntities;
