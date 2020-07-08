class PiiAppClient {
  constructor (host) {
    this.host = host
  }

  replaceTicketId (payload) {
    const jsonifyBody = JSON.stringify(payload['ticket.id'])

    return fetch(`${this.host}/update-ticket-id`, {
      method: 'PUT',
      body: jsonifyBody,
      cache: 'no-cache',
      headers: {
        'Content-Type': 'application/json'
      }
    })
  }
}

export { PiiAppClient }
