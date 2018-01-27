// import {observable} from 'mobx';
import {ServerFetch} from './types';
declare var window: any;

// let serverMessage = observable.ref(null);
// export const connected = observable(false);
// const wsUrl = `ws://${window.commandLineArgs.address}/ws`;
const wsUrl = `ws://localhost:3922`;
console.log(wsUrl)
export const ws = new WebSocket(wsUrl);
// const serverMessageQueue: string[] = [];
const outstandingFetches = new Map<string, ServerFetch>();

ws.onopen = () => {
    console.log('p')
//     // connected.set(true);
//     for (let msg of serverMessageQueue) {
//         ws.send(msg);
//         console.log('m', msg);
//     }
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
        // serverMessage = msg;
    }
}
 
export function wsFetch(type: string, args: any = [], kwargs: any = {}) {
    if (ws.readyState !== WebSocket.OPEN) {
        throw "Websocket connection not open";
    }
    const id = generateUUID();
    const msgString = JSON.stringify({type, id, args, kwargs});
    const timestamp = Date.now();
    ws.send(msgString);
    const respPromise = new Promise((resolve, reject) => {
        const sf: ServerFetch = {timestamp, resolve, reject};
        outstandingFetches.set(id, sf);
    });
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