import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { ModalHeader, ModalBody, ModalFooter, Button } from 'reactstrap'
import ActionList from './action-list';
import RuleInput from './rule-input';
import ActionEditor from './action-editor'
import { CommandEditorProps, CommandEditorState } from "./types";
import { cloneDeep } from "lodash";

class CommandEditor extends React.Component<CommandEditorProps, CommandEditorState> {

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
                    <RuleInput rule={this.props.command.rule} />
                    <ActionList actions={this.props.command.action} />
                    <ActionEditor />
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