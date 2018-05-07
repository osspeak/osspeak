import {remote} from 'electron'
declare var window: any;
const args = remote.getGlobal('args')

window.commandLineArgs = JSON.parse(args[2]);