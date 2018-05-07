export interface CommandModuleContainerProps {
    commandModules: any    
}

export interface CommandModuleContainerState {
    selectedCommandModule: null | string
    activeCommandModules: string[]
}

export interface CommandModule {
    id: string
}