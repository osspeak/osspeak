export interface CommandModule {
    path: string
    config: CommandModuleConfig
}

export interface CommandModuleConfig {
    commands: [string, string | ActionPieceConfig[]]
    rules?: Rule[]
    functions?: any[]
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
export interface ActionPieceConfig {
    type: 'dsl'
    value: any
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
