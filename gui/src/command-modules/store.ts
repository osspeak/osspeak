import {observable, computed, action, runInAction} from 'mobx';
import {CommandModulesStoreInterface} from './types';

console.log(runInAction)
class CommandModulesStore implements CommandModulesStoreInterface {
    
    @action.bound
    async fetchCommandModuleTree() {

    }
}

export default new CommandModulesStore();