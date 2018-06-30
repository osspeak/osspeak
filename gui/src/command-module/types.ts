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
export interface Command {
    rule: Rule
    action: any
}

export interface Rule {
    text: string
}
export interface Action {
    pieces: any[]
}

export interface RecognitionIndex {
    commandModules: { [s: string]: CommandModule },
    osSep: string
}

export interface CommandModulePanelProps {
    commandModule: CommandModule
}

export interface CommandModuleTabsProps {
    selected: string
    onTabClick: (name: string) => void
    paths: string[]
}

export interface CommandEditorProps {
    command: Command
 }

export interface CommandEditorState {

 }