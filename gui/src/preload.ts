import {remote} from 'electron'
declare var window: any;
const args = remote.getGlobal('args')
window.commandLineArgs = {
    address: args[2]   
};