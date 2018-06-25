export interface CommandModuleContainerProps {
    recognitionIndex: RecognitionIndex
}

export interface CommandModuleContainerState {
    selectedPath: null | string
    activePaths: string[]
}

export interface CommandModule {
    id: string
}

export interface RecognitionIndex {
    commandModules: { [s: string]: CommandModule },
    osSep: string
}

export interface CommandModulePanelProps {
    commandModule: CommandModule
}