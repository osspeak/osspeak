export interface CommandModule {
    path: string
    config: CommandModuleConfig
}

export interface CommandModuleConfig {
    commands: Command[]
} 

export interface Command {
    rule: Rule
    action: Action
}

export interface Rule {
    text: string
}
export interface Action {
    pieces: ActionPiece[]
}
export interface ActionPiece {
    type: 'dsl'
    value: any
}

export interface RecognitionIndex {
    commandModules: { [path: string]: CommandModuleConfig },
    activeCommandModules: string[],
    osSep: string
}
