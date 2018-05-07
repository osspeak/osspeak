import { NormalizedObjects } from "../types";

export interface CommandModuleContainerProps {
    
}

export interface CommandModuleContainerState {

}

export interface CommandModuleState {
    modules: NormalizedObjects<CommandModule>
    selected?: string
    osSep?: string
}

export interface CommandModule {
    id: string
}