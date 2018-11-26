function setupConnection() {
  /*
    Setup a connection to receive all the information
    about the webhooks in real-time.
  */
  var callbackCode = getCallbackCode();
  console.log(callbackCode);

  var webhookSocket = new WebSocket(
    "ws://" + window.location.host + "/ws/callback/" + callbackCode + "/"
  );

  webhookSocket.onmessage = function(event) {
    /*
        Parses the information adds it to the UI state
    */
    console.log(event);
  };
  webhookSocket.onopen = function(event) {
    console.log("[Webhook_logger] Connection stablished");
  };
  webhookSocket.onclose = function(event) {
    console.log("[Webhook_logger] Connection lost");
    console.log("[Webhook_logger] Trying to reconnect");
    setupConnection();
  };
}

function getCallbackCode() {
  var urlParams = new URLSearchParams(window.location.search);
  return urlParams.get("cb");
}

setupConnection();
