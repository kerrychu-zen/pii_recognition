import client from "./zafClient.js";

const getCommentTexts = async () => {
  // TODO: add error handle
  const response = await client.get("ticket.comments");
  const ticketComments = response["ticket.comments"];
  // note text contains HTML
  const commentTexts = ticketComments.map((comment) => comment.value);
  return commentTexts;
};

const getComments = async () => {
  // TODO: add error handle
  const response = await client.get("ticket.comments");
  const comments = response["ticket.comments"];
  const commentIdValue = comments.map((comment) => ({
    id: comment.id,
    text: comment.value,
  }));

  return commentIdValue;
};

const getTicketId = async () => {
  // TODO: add error handle
  const response = await client.get("ticket.id");
  return response["ticket.id"];
};

const requestRedactApi = async (ticketId, commentId, text) => {
  let response;
  let options = {
    url: `/api/v2/tickets/${ticketId}/comments/${commentId}/redact.json`,
    type: "PUT",
    contentType: "application/json",
    data: JSON.stringify({ text: `${text}` }),
  };

  // TODO: are we satisfied with this error handler?
  try {
    response = await client.request(options);
  } catch (err) {
    console.log("redaction error: ", err);
  }
};

export { getCommentTexts, getComments, getTicketId, requestRedactApi };
