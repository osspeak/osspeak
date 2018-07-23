import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../server';
import { ModalHeader, ModalBody, ModalFooter, Button } from 'reactstrap'
import ActionPieceList from './action-piece-list';
import RuleInput from './rule-input';
import ActionPieceEditor from './action-piece-editor'
import {Command, Rule, Action } from "./types";
import { cloneDeep } from "lodash";

export interface CommandEditorProps {
    command: Command
    save: any
 }

export interface CommandEditorState {
    action: Action
    rule: Rule
 }

class CommandEditor extends React.Component<CommandEditorProps, CommandEditorState> {

    constructor(props: CommandEditorProps) {
        super(props);
        const {action, rule} = cloneDeep(props.command)
        this.state = {
            action,
            rule
        }
    }

    onRuleTextChanged = (text: string) => {
        const rule = {...this.state.rule, text}
        this.setState({rule})
    }

    save = () => {
        const command = {...this.state}
        this.props.save(command);
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
                    <RuleInput onChange={this.onRuleTextChanged} text={this.state.rule.text} />
                    <ActionPieceList actionPieces={this.state.action.pieces} />
                    <ActionPieceEditor />
                </ModalBody>
                <ModalFooter>
                    <Button color="primary" onClick={this.save}>Save</Button>{' '}
                    <Button color="secondary" onClick={this.toggle}>Cancel</Button>
                </ModalFooter>
            </>
        );
    }
}

export default CommandEditor;