/*
  Utility functions to help with some common tasks.
*/
function logger(message) {
  let datetime = new Date().toISOString();
  console.log(`[Webhook_logger] [${datetime}] ${message}`);
}

function getCallbackCode() {
  let urlParams = new URLSearchParams(window.location.search);
  return urlParams.get("cb");
}

/*
  Connection setup. All code that handles the websocket traffic.
*/
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
  Create the highlight directive
*/
Vue.directive("highlightjs", {
  deep: true,
  bind: function(el, binding) {
    if (binding.value) {
      el.textContent = binding.value;
    }
    hljs.highlightBlock(el);
  },
  componentUpdated: function(el, binding) {
    if (binding.value) {
      target.textContent = binding.value;
      hljs.highlightBlock(target);
    }
  }
});

/*
  Setup a simple components to handle the display of new content.
*/
var requestList = new Vue({
  el: "#request-list",
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

var callbackDetails = new Vue({
  el: "#callback-details",
  delimiters: ["[[", "]]"],
  data: {
    callback_url: "",
    show_copy_notification: false
  },
  methods: {
    copytoclipboard: function() {
      var url = document.getElementById("callback-uuid-field");
      url.select();
      document.execCommand("copy");
      this.show_copy_notification = true;
      let self = this;
      setTimeout(function() {
        self.show_copy_notification = false;
      }, 2000);
    }
  },
  mounted: function() {
    let protocol = document.location.protocol;
    let host = document.location.host;
    this.callback_url = `${protocol}//${host}/${getCallbackCode()}`;
  }
});

/*
  Prepare the page for action
*/
setupConnection();
