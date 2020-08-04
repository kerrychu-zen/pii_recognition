import { comprehendClient } from "./awsClients.js";

const detectPiiEntities = async (text, language = "en") => {
  let params = {
    Text: text,
    LanguageCode: language,
  };

  const request = comprehendClient.detectEntities(params);
  // TODO: add error handle
  const response = await request.promise();
  const entityArray = response["Entities"].map((entity) => entity["Text"]);

  return entityArray;
};

export { detectPiiEntities };
