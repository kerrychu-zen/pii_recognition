import { PiiAppClient } from './piiAppClient.js'

const forwardTicketId = function (zafClient, appClient) {
  zafClient.get('ticket.id')
    .then(payload => appClient.replaceTicketId(payload))
    .then(response => {
      if (response.status !== 200) {
        console.log(`Request failed. Status code: ${response.status}`)
      }
    })
    .catch(error => console.log(error))
}

const zafClient = ZAFClient.init() // takes some time to initialise
const appClient = new PiiAppClient(window.origin)

forwardTicketId(zafClient, appClient)
