import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../server';
import { Modal } from 'reactstrap'
import CommandPreview from './command-preview';
import { CommandModule } from "./types";
import CommandEditor from "./command-editor";

export interface CommandModulePanelProps {
    commandModule: CommandModule
    save: any
}
export interface CommandModulePanelState {
    commandBeingEditedIndex: number | null
}

class CommandModulePanel extends React.Component<CommandModulePanelProps, CommandModulePanelState> {

    constructor(props: any) {
        super(props);
        this.state = {commandBeingEditedIndex: null};
    }

    onModuleSelected = (index: number) => {
        this.setState({ commandBeingEditedIndex: index })
    }

    toggle = () => {
        this.setState({ commandBeingEditedIndex: null });
    }

    render() {
        const { commands } = this.props.commandModule.config;
        const editIndex = this.state.commandBeingEditedIndex
        const commandBeingEdited = editIndex === null ? null : commands[editIndex]
        return (
            <div id="command-module-panel">
                {commands.map((cmd: any, i: number) =>
                    <CommandPreview key={i.toString()} command={cmd} onSelect={() => this.onModuleSelected(i)} />
                )}
                <Modal isOpen={commandBeingEdited !== null} toggle={this.toggle}>
                    {commandBeingEdited && <CommandEditor save={this.props.save} index={editIndex as number} command={commandBeingEdited} />}
                </Modal>
            </div>
        );
    }
}

export default CommandModulePanel;