import { wsFetch } from '../websocket'
import { normalize, emptyNormalized } from "../util";
import { CommandModuleState, CommandModule } from "./types";

const SET_PATHS = 'osspeak/command-module/SET_PATHS';

// Reducer
export default function reducer(state = initialState(), action: any = {}): CommandModuleState {
    switch (action.type) {
        // do reducer stuff
        case SET_PATHS:
            const moduleArray: CommandModule[] = action.paths.map((p: string) => {
                return {id: p}
            });
            const modules = normalize(moduleArray);
            return {...state, modules, osSep: action.osSep}
        default:
            return state;
    }
}

// Action Creators

export function setCommandModulePaths(paths: string[], osSep: string) {
    return { type: SET_PATHS, paths, osSep };
}

export function loadCommandModulePaths() {
    return async (dispatch: any) => {
        const {paths, osSep} = await wsFetch('COMMAND_MODULE_PATHS');
        dispatch(setCommandModulePaths(paths, osSep))
    }
}

function initialState(): CommandModuleState {
    return {
        modules: emptyNormalized(),

    }
}