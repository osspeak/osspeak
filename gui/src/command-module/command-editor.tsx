import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { ModalHeader, ModalBody, ModalFooter, Button } from 'reactstrap'
import ActionList from './action-list';
import { CommandModulePanelProps } from "./types";

class CommandEditor extends React.Component<any, any> {

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
        // const { commands } = this.props.module;
        return (
            <>
                <ModalHeader toggle={this.toggle}>Edit Command</ModalHeader>
                <ModalBody>
                    <ActionList />
                </ModalBody>
                <ModalFooter>
                    <Button color="primary" onClick={this.toggle}>Do Something</Button>{' '}
                    <Button color="secondary" onClick={this.toggle}>Cancel</Button>
                </ModalFooter>
            </>
        );
    }
}

export default CommandEditor;