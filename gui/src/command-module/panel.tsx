import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { Modal } from 'reactstrap'
import CommandPreview from './command-preview';
import { CommandModulePanelProps } from "./types";

class CommandModulePanel extends React.Component<any, any> {

    constructor(props: any) {
        super(props);
        this.state = {
            commandBeingEditedIndex: null,
        }
    }

    onModuleSelected = (index: Number) => {
        this.setState({ commandBeingEditedIndex: index })
    }

    toggle = () => {
        this.setState({commandBeingEditedIndex: null});
    }

    render() {
        const { commands } = this.props.module;
        return (
            <div id="command-module-panel">
                {commands.map((cmd: any, i: Number) =>
                    <CommandPreview key={i.toString()} command={cmd} onSelect={() => this.onModuleSelected(i)} />
                )}
                <Modal isOpen={this.state.commandBeingEditedIndex !== null} toggle={this.toggle} className={this.props.className}>
                    modal content
                    {/* <ModalHeader toggle={this.toggle}>Modal title</ModalHeader>
          <ModalBody>
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
          </ModalBody>
          <ModalFooter>
            <Button color="primary" onClick={this.toggle}>Do Something</Button>{' '}
            <Button color="secondary" onClick={this.toggle}>Cancel</Button>
          </ModalFooter> */}
                </Modal>
            </div>
        );
    }
}

export default CommandModulePanel;