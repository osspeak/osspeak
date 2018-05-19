export interface CommandModuleContainerProps {
    commandModules: any    
}

export interface CommandModuleContainerState {
    selectedPath: null | string
    activePaths: string[]
}

export interface CommandModule {
    id: string
}