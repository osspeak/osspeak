import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { Modal } from 'reactstrap'
import CommandPreview from './command-preview';
import { CommandModulePanelProps } from "./types";
import CommandEditor from "./command-editor";

class CommandModulePanel extends React.Component<any, any> {

    state = {
        commandBeingEditedIndex: null,
    }

    constructor(props: any) {
        super(props);
    }

    onModuleSelected = (index: Number) => {
        this.setState({ commandBeingEditedIndex: index })
    }

    toggle = () => {
        this.setState({ commandBeingEditedIndex: null });
    }

    render() {
        const { commands } = this.props.module;
        const editIndex = this.state.commandBeingEditedIndex
        const commandBeingEdited = editIndex === null ? null : commands[editIndex]
        return (
            <div id="command-module-panel">
                {commands.map((cmd: any, i: Number) =>
                    <CommandPreview key={i.toString()} command={cmd} onSelect={() => this.onModuleSelected(i)} />
                )}
                <Modal isOpen={commandBeingEdited !== null} toggle={this.toggle} className={this.props.className}>
                    <CommandEditor command={commandBeingEdited} />
                </Modal>
            </div>
        );
    }
}

export default CommandModulePanel;