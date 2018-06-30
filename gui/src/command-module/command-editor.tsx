import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { ModalHeader, ModalBody, ModalFooter, Button } from 'reactstrap'
import ActionPieceList from './action-piece-list';
import RuleInput from './rule-input';
import ActionPieceEditor from './action-piece-editor'
import {Command } from "./types";
import { cloneDeep } from "lodash";

export interface CommandEditorProps {
    command: Command
 }

export interface CommandEditorState {
    commandCopy: Command
 }

class CommandEditor extends React.Component<CommandEditorProps, CommandEditorState> {

    constructor(props: CommandEditorProps) {
        super(props);
        this.state = {
            commandCopy: cloneDeep(props.command)
        }
    }

    toggle = () => {
    }

    render() {
        // const { commands } = this.props.module;
        return (
            <>
                <ModalHeader toggle={this.toggle}>Edit Command</ModalHeader>
                <ModalBody>
                    <RuleInput text={this.props.command.rule.text} />
                    <ActionPieceList actionPieces={this.props.command.action.pieces} />
                    <ActionPieceEditor />
                </ModalBody>
                <ModalFooter>
                    <Button color="primary" onClick={this.toggle}>Save</Button>{' '}
                    <Button color="secondary" onClick={this.toggle}>Cancel</Button>
                </ModalFooter>
            </>
        );
    }
}

export default CommandEditor;