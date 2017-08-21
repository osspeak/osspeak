import {observable, computed, action, runInAction} from 'mobx';
import {CommandModulesStoreInterface} from './types';
import {wsFetch} from '../websocket';

console.log(runInAction)
class CommandModulesStore implements CommandModulesStoreInterface {
    
    @action.bound
    async fetchCommandModuleTree() {
        const resp = await wsFetch('GET_COMMAND_MODULES');
        console.log('fcmt', resp)
    }
}

export default new CommandModulesStore();