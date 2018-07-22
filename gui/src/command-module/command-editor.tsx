import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../server';
import { ModalHeader, ModalBody, ModalFooter, Button } from 'reactstrap'
import ActionPieceList from './action-piece-list';
import RuleInput from './rule-input';
import ActionPieceEditor from './action-piece-editor'
import {Command } from "./types";
import { cloneDeep } from "lodash";

export interface CommandEditorProps {
    index: number
    command: Command
    save: any
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

    save = async () => {
    //     console.log('save')
    //     const toUpdate = {[this.props.command}
    //     const res = await wsFetch('SAVE_COMMAND_MODULES', );
    }

    toggle = () => {
    }

    render() {
        // const { commands } = this.props.module;
        return (
            <>
                <ModalHeader toggle={this.toggle}>Edit Command</ModalHeader>
                <ModalBody>
                    <RuleInput text={this.state.commandCopy.rule.text} />
                    <ActionPieceList actionPieces={this.state.commandCopy.action.pieces} />
                    <ActionPieceEditor />
                </ModalBody>
                <ModalFooter>
                    <Button color="primary" onClick={this.props.save}>Save</Button>{' '}
                    <Button color="secondary" onClick={this.toggle}>Cancel</Button>
                </ModalFooter>
            </>
        );
    }
}

export default CommandEditor;