import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../server';
import { Modal } from 'reactstrap'
import CommandPreview from './command-preview';
import { CommandModule, Command } from "./types";
import CommandModulePanel from "./panel";

export interface CommandModuleContainerProps {
    commandModule: CommandModule
}
export interface CommandModuleContainerState {
}

class CommandModuleContainer extends React.Component<CommandModuleContainerProps, CommandModuleContainerState> {

    constructor(props: any) {
        super(props);
    }

    save = async () => {
        const kwargs = {}
        const toUpdate = [this.props.commandModule]
        const result = await wsFetch('SAVE_MODULE_CHANGES', [toUpdate, []]);
        console.log('save', result);
    }

    render() {
        console.log(this.props.commandModule.path, 'abc')
        return <CommandModulePanel save={this.save} commandModule={this.props.commandModule} />
    }
}

export default CommandModuleContainer;