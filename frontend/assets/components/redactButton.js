import { getComments, getTicketId, requestRedactApi } from "../apis/zafApis.js";
import { removeWhitespace } from "../utils.js";
import { entitiesStringSplitDelimiter } from "../constants.js";
import client from "../apis/zafClient.js";

const redact = async (text) => {
  const ticketId = await getTicketId();
  const comments = await getComments();

  const texts = text.split(entitiesStringSplitDelimiter).map(removeWhitespace);

  for (const comment of comments) {
    for (const text of texts) {
      if (comment["text"].includes(text)) {
        await requestRedactApi(ticketId, comment["id"], text);
      }
    }
  }

  client.invoke('notify', 'Redaction done!');
};

export default redact;
