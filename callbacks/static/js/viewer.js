function logger(message) {
  let datetime = new Date().toISOString();
  console.log(`[Webhook_logger] [${datetime}] ${message}`);
}

function getCallbackCode() {
  let urlParams = new URLSearchParams(window.location.search);
  return urlParams.get("cb");
}

function setCallbackUrl(callbackCode) {
  let protocol = document.location.protocol;
  let host = document.location.host;
  let submitURL = `${protocol}//${host}/${getCallbackCode()}`;
  document.getElementById("callback-uuid-field").value = submitURL;
}

function setupConnection() {
  /*
    Setup a connection to receive all the information
    about the webhooks in real-time.
  */
  let protocol = document.location.protocol == "https:" ? "wss://" : "ws://";
  let callbackCode = getCallbackCode();
  let webhookSocket = new WebSocket(
    protocol + window.location.host + "/ws/callback/" + callbackCode + "/"
  );

  webhookSocket.onmessage = function(event) {
    /*
      Parses the information adds it to the UI state
    */
    logger("Message Received");
    requestList.addRequest(JSON.parse(event.data));
  };

  webhookSocket.onopen = function(event) {
    logger("Connection stablished");
  };

  webhookSocket.onclose = function(event) {
    logger("Connection lost");
    logger("Trying to reconnect");
    setupConnection();
  };
}

/*
  Setup a simple component to handle the display of new content.
  Only supports two functions:
  - Add new content
  - Clean existing content
*/
var requestList = new Vue({
  el: "#app",
  delimiters: ["[[", "]]"],
  data: {
    requests: []
  },
  methods: {
    addRequest: function(request) {
      request.displayFull = false;
      this.requests.unshift(request);
    },
    toggleDetail: function(index) {
      let req = this.requests[index];
      req.displayFull = !req.displayFull;
    },
    removeItem: function(index) {
      this.requests.splice(index, 1);
    },
    clean: function() {
      this.requests = [];
    },
    download: function() {
      let data = JSON.stringify(this.requests);
      let encoded_data = encodeURIComponent(data);

      let element = document.createElement("a");
      element.setAttribute("href", "data:text/plain;charset=utf-8," + data);
      element.setAttribute("download", "requests.json");

      element.style.display = "none";
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    }
  }
});

/*
  Prepare the page for action
*/
setCallbackUrl();
setupConnection();
