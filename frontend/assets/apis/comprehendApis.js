import { comprehendClient } from "./awsClients.js";
import { handle } from "../utils.js";

// TODO: second pass generalise this interface
const detectPiiEntities = async (text, language = "en", threshold = 0.9) => {
  let params = {
    Text: text,
    LanguageCode: language,
  };

  const request = comprehendClient.detectEntities(params);
  const [response, err] = await handle(request.promise());
  if (err) throw new Error("Could not run comprehend for entity detection");

  // if no entities found this returns []
  const entityArray = response["Entities"]
    .filter((entity) => entity["Score"] > threshold)
    .map((entity) => entity["Text"]);
  const uniqueEntities = Array.from(new Set(entityArray));

  return uniqueEntities;
};

export { detectPiiEntities };
