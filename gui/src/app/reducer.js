import { combineReducers } from 'redux';
import { commandModulesReducer } from '../command-modules/reducers';

export function mainReducer() {
    return combineReducers({
        commandModules: commandModulesReducer
    });
}