import {ServerFetch} from './types';
declare var window: any;

// let serverMessage = observable.ref(null);
// export const connected = observable(false);
// const wsUrl = `ws://${window.commandLineArgs.address}/ws`;
const wsUrl = `ws://localhost:3922`;
export const ws = new WebSocket(wsUrl);
const outstandingFetches = new Map<string, ServerFetch>();
const remote = require('electron').remote;

ws.onopen = () => {
    (async() => {
    })()
}

ws.onmessage = (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.hasOwnProperty('id')) {
        if (!outstandingFetches.has(msg.id)) throw `Missing response id: ${msg.id}`;
        const sf = outstandingFetches.get(msg.id) as ServerFetch;
        outstandingFetches.delete(msg.id);
        if (msg.ok) sf.resolve(msg.data);
        else sf.reject(msg.data);
    }
    else {
        //serverMessage;
    }
}

ws.onclose = () => {
    var window = remote.getCurrentWindow();
    window.close();
}
 
export function wsFetch(resource: string, args: any = [], kwargs: any = {}) {
    if (ws.readyState !== WebSocket.OPEN) {
        throw "Websocket connection not open";
    }
    const id = generateUUID();
    const msgString = JSON.stringify({resource, id, args, kwargs});
    const timestamp = Date.now();
    const respPromise = new Promise<any>((resolve, reject) => {
        const sf: ServerFetch = {timestamp, resolve, reject};
        outstandingFetches.set(id, sf);
    });
    ws.send(msgString);
    return respPromise;
}

function generateUUID () {
    let d = new Date().getTime();
    d += performance.now();
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        let r = (d + Math.random() * 16) % 16 | 0;
        d = Math.floor(d / 16);
        return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
}