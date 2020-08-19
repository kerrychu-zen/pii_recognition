import { getCommentTexts } from "../apis/zafApis.js";
import { stripHtml, concatStrings } from "../utils.js";
import { commentsConcatDelimiter } from "../constants.js";
import models from "./dropdown.js";

const textPreprocessor = (texts) => {
  const cleanTexts = texts.map((text) => stripHtml(text));
  return concatStrings(cleanTexts, commentsConcatDelimiter);
};

const predictPiiEntities = (text, modelName) => {
  return models[modelName.toLowerCase()](text);
};

const getPiiEntities = async (modelName) => {
  const comments = await getCommentTexts();
  const concatenatedComments = textPreprocessor(comments);
  const entities = predictPiiEntities(concatenatedComments, modelName);
  return entities;
};

export default getPiiEntities;
