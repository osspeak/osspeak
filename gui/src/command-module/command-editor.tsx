import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../server';
import { ModalHeader, ModalBody, ModalFooter, Button } from 'reactstrap'
import ActionPieceList from './action-piece-list';
import RuleInput from './rule-input';
import ActionPieceEditor from './action-piece-editor'
import { Command, Rule, Action, ActionPiece } from "./types";
import { cloneDeep, pickBy } from "lodash";

export interface CommandEditorProps {
    command: Command
    save: any
    toggle: () => any
}

export interface CommandEditorState {
    actionPieces: ActionPiece[]
    rule: Rule
    selectedActionPieceIndex: null | number
}

class CommandEditor extends React.Component<CommandEditorProps, CommandEditorState> {

    constructor(props: CommandEditorProps) {
        super(props);
        const {action, rule} = cloneDeep(props.command)
        this.state = {
            actionPieces: action.pieces,
            rule,
            selectedActionPieceIndex: null,
        }
    }

    onActionPieceClick = (index: number) => {
        this.setState({ selectedActionPieceIndex: index });
    }

    onRuleTextChanged = (text: string) => {
        const rule = { ...this.state.rule, text }
        this.setState({rule});
    }

    get command(): Command {
        const {actionPieces, rule} = {...this.state}
        const action: Action = {pieces: actionPieces}
        return {
            action,
            rule
        }
    }

    save = () => {
        this.props.save(this.command);
        // this.props.save(this.state.editedCommand);
        //     console.log('save')
        //     const toUpdate = {[this.props.command}
        //     const res = await wsFetch('SAVE_COMMAND_MODULES', );
    }

    onActionPieceChange = (value: any) => {
        const index = this.state.selectedActionPieceIndex;
        if (index === null) return;
        const actionPieces = [...this.state.actionPieces];
        actionPieces[index] = {...actionPieces[index], value};
        this.setState({actionPieces});
    }

    toggle = () => {
    }

    render() {
        // const { commands } = this.props.module;
        const {rule, actionPieces, selectedActionPieceIndex} = this.state;
        const selectedActionPiece = this.state.selectedActionPieceIndex === null ? null : actionPieces[this.state.selectedActionPieceIndex]
        return (
            <>
                <ModalHeader toggle={this.toggle}>Edit Command</ModalHeader>
                <ModalBody>
                    <RuleInput onChange={this.onRuleTextChanged} text={rule.text} />
                    <ActionPieceList
                        onPieceClick={this.onActionPieceClick}
                        actionPieces={actionPieces}
                        selectedIndex={selectedActionPieceIndex}
                    />
                    {selectedActionPiece && <ActionPieceEditor piece={selectedActionPiece} onChange={this.onActionPieceChange} />}
                </ModalBody>
                <ModalFooter>
                    <Button color="primary" onClick={this.save}>Save</Button>{' '}
                    <Button color="secondary" onClick={this.props.toggle}>Cancel</Button>
                </ModalFooter>
            </>
        );
    }
}

export default CommandEditor;