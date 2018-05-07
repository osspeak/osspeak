import { CommandModuleState } from './command-module/types';

export interface ServerFetch {
    timestamp: number
    resolve: any
    reject: any
}

export interface ApplicationState {
    modules: CommandModuleState
}

export interface NormalizedObjects<T> {
    byId: {
        [id: string]: T
    };
    allIds: string[];
}