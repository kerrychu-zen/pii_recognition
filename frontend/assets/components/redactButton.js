import { getComments, getTicketId, requestRedactApi } from "../apis/zafApis.js";

const redact = async (text) => {
  const ticketId = await getTicketId();
  const comments = await getComments();

  // TODO: DO NOT hard code split delimiter
  const texts = text.split(",").map((text) => text.trim());

  for (const comment of comments) {
    for (const text of texts) {
      if (comment["text"].includes(text)) {
        await requestRedactApi(ticketId, comment["id"], text);
      }
    }
  }

  // TODO: use Garden notification
  console.log("Redaction done!");
};

export default redact;
