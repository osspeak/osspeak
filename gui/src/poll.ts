import {observable} from 'mobx';
declare var window: any;

let serverPushMessage = observable.ref(null);

export async function pollServer() {
    const url = `${window.commandLineArgs.address}/poll`;
    let error: string = null;
    try {
        const resp = await fetch(url);
    }
    catch(e) {
        error = e;
    }
    let pollTimeout = 0;
    if (error !== null) {
        pollTimeout = 10000;
        console.log(error);
    }
    serverPushMessage = 5;
    setTimeout(pollServer, pollTimeout);
}