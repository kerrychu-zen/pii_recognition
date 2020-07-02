var client = ZAFClient.init();
var url = `${window.origin}/update_ticket_id`

var ticket_id = client.get('ticket.id').then(
    function(data) {
        return fetch(url, {
            method: "POST",
            body: JSON.stringify(data['ticket.id']),
            cache: "no-cache",
            headers: {'Content-Type': 'application/json'},
        });
    }).then(function (response) {
        if (response.status !== 204) {
            console.log(`Request failed. Status code: ${response.status}`);
            return;
        } 
    }).catch(function (error) {
        console.log(error);
    });

