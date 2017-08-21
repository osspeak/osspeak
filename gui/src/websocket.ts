import {observable} from 'mobx';
import {ServerFetch} from './types';
declare var window: any;

let serverMessage = observable.ref(null);
export const connected = observable(false);
const wsUrl = `ws://${window.commandLineArgs.address}/ws`;
export const ws = new WebSocket(wsUrl);
const serverMessageQueue: string[] = [];
const outstandingFetches = new Map<string, ServerFetch>();

ws.onopen = () => {
    connected.set(true);
    for (let msg of serverMessageQueue) {
        ws.send(msg);
        console.log('m', msg);
    }
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
        serverMessage = msg;
    }
}

export async function wsFetch(type: string, data: any = {}) {
    const id = generateUUID();
    const msgString = JSON.stringify({type, id, data});
    const timestamp = Date.now();
    if (ws.readyState === 0) {
        serverMessageQueue.push(msgString);
    }
    else if (ws.readyState === 1) {
        ws.send(msgString);
    }
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