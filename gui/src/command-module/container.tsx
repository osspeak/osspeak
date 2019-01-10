import React from 'react';
import { wsFetch } from '../server';
import { CommandModule, Command } from "./types";
import CommandModulePanel from "./panel";
import {cloneDeep} from 'lodash'

export interface CommandModuleContainerProps {
    commandModule: CommandModule
}
export interface CommandModuleContainerState {
    commands: Command[]
}

class CommandModuleContainer extends React.Component<CommandModuleContainerProps, CommandModuleContainerState> {

    constructor(props: CommandModuleContainerProps) {
        super(props);
        const {commands} = cloneDeep(props.commandModule.config)
        this.state = {
            commands
        }
    }

    updateCommand = async (command: Command, index: number) => {
        const commands = [...this.state.commands];
        commands[index] = command;
        const args = [command, index, this.props.commandModule.path]
        const result = await wsFetch('SAVE_COMMAND', args);
        this.setState({commands}, this.saveModule);
    }

    saveModule = async () => {
        const toUpdate = [this.props.commandModule]
        console.log('ti', toUpdate[0]);
        // const result = await wsFetch('SAVE_MODULE_CHANGES', [toUpdate, []]);
        // console.log('save', result);
    }

    render() {
        return <CommandModulePanel updateCommand={this.updateCommand} commands={this.state.commands} />
    }
}

export default CommandModuleContainer;