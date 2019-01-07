import React from 'react';
import { wsFetch } from '../server';
import { Modal } from 'reactstrap'
import CommandPreview from './command-preview';
import { CommandModule, Command } from "./types";
import CommandEditor from "./command-editor";

export interface CommandModulePanelProps {
    commands: Command[]
    updateCommand: any
}
export interface CommandModulePanelState {
    commandBeingEditedIndex: number | null
}

class CommandModulePanel extends React.Component<CommandModulePanelProps, CommandModulePanelState> {

    constructor(props: CommandModulePanelProps) {
        super(props);
        this.state = {
            commandBeingEditedIndex: null
        };
    }

    updateCommand = (command: Command) => {
        this.props.updateCommand(command, this.state.commandBeingEditedIndex);
        this.setState({commandBeingEditedIndex: null});
    }

    onModuleSelected = (index: number) => {
        this.setState({ commandBeingEditedIndex: index })
    }

    toggle = () => {
        this.setState({ commandBeingEditedIndex: null });
    }

    render() {
        const editIndex = this.state.commandBeingEditedIndex;
        const commandBeingEdited = editIndex === null ? null : this.props.commands[editIndex];
        return (
            <div id="command-module-panel">
                {this.props.commands.map((cmd, i) =>
                    <CommandPreview key={i.toString()} command={cmd} onSelect={() => this.onModuleSelected(i)} />
                )}
                <Modal isOpen={commandBeingEdited !== null} toggle={this.toggle}>
                    {commandBeingEdited && <CommandEditor
                        save={this.updateCommand}
                        command={commandBeingEdited}
                        toggle={this.toggle}
                    />}
                </Modal>
            </div>
        );
    }
}

export default CommandModulePanel;