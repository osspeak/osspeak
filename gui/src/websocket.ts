import {observable} from 'mobx';
declare var window: any;

let serverMessage = observable.ref(null);
export const connected = observable(false);
const wsUrl = `ws://${window.commandLineArgs.address}/ws`;
export const ws = new WebSocket(wsUrl);

ws.onopen = () => {
    connected.set(true);
    console.log('sdfsdf')
    wsFetch('FOO')
}

export async function wsFetch(type: string, data: any = {}) {
    const id = generateUUID();
    const msgString = JSON.stringify({type, id, data})
    ws.send(msgString)
}

function generateUUID () { // Public Domain/MIT
    let d = new Date().getTime();
    d += performance.now(); //use high-precision timer if available
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        let r = (d + Math.random() * 16) % 16 | 0;
        d = Math.floor(d / 16);
        return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
}