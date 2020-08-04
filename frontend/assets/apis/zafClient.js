let client;

if (typeof ZAFClient === "undefined") {
  throw new Error("ZAFClient cannot run outside Zendesk");
} else {
  client = ZAFClient.init();
}

export default client;
