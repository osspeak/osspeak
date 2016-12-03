class MainProcessCommunicator {

    constructor(address) {
        this.address = address;
        this.subscriptions = new Map();
        this.startWebSocket();
    }

    startWebSocket() {
        this.ws = new WebSocket(this.address);
        this.ws.onopen = this.onopen.bind(this);
        this.ws.onmessage = this.onmessage.bind(this);
    }

    onopen() {
        this.ws.send('sasdasdsad');
    }

    fireSubscription(name, payload) {
        if (!this.subscriptions.has(name)) return;
        this.subscriptions.get(name)(payload);
    }

    onmessage(msg) {
        const msgObj = JSON.parse(msg.data);
        this.fireSubscription(msgObj.type, msgObj.payload);
        console.log(msgObj);
    }

    sendMessage(msg, payload={}) {
        const fullMsg = JSON.stringify({type: msg, payload: payload});
        this.ws.send(fullMsg)
    }

}