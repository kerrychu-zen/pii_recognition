import { comprehendClient } from "./awsClients.js";
import { handle } from "../utils.js";

// TODO: second pass generalise this interface
const detectPiiEntities = async (text, language = "en") => {
  let params = {
    Text: text,
    LanguageCode: language,
  };

  // TODO: 
  // 1. language detection for multilingual
  // 2. Thresholding
  // 3. Named entity types
  const request = comprehendClient.detectEntities(params);
  const [response, err] = await handle(request.promise());
  if (err) throw new Error("Could not run comprehend for entity detection");

  // if no entities found this returns []
  var entities = response["Entities"].map((entity) => entity["Text"])
  const entityArray = Array.from(new Set(entities));

  return entityArray;
};

export { detectPiiEntities };
