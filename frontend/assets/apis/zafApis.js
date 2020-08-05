import client from "./zafClient.js";
import { handle } from "../utils.js";

const getCommentTexts = async () => {
  const [response, err] = await handle(client.get("ticket.comments"));
  if (err) throw new Error("Could not get comment strings");
  const ticketComments = response["ticket.comments"];
  // note text contains HTML
  const commentTexts = ticketComments.map((comment) => comment.value);
  return commentTexts;
};

const getComments = async () => {
  const [response, err] = await handle(client.get("ticket.comments"));
  if (err) throw new Error("Could not get comments");
  const comments = response["ticket.comments"];
  const commentIdValue = comments.map((comment) => ({
    id: comment.id,
    text: comment.value,
  }));

  return commentIdValue;
};

const getTicketId = async () => {
  const [response, err] = await handle(client.get("ticket.id"));
  if (err) throw new Error("Could not get comments");
  return response["ticket.id"];
};

const requestRedactApi = async (ticketId, commentId, text) => {
  let options = {
    url: `/api/v2/tickets/${ticketId}/comments/${commentId}/redact.json`,
    type: "PUT",
    contentType: "application/json",
    data: JSON.stringify({ text: `${text}` }),
  };

  const [_, err] = await handle(client.request(options));
  if (err) {
    if (err.status == 400) {
      console.log("Text not found");
    } else {
      throw new Error("Redaction error");
    }
  }
};

export { getCommentTexts, getComments, getTicketId, requestRedactApi };
