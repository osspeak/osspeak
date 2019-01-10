import React from 'react';
import ReactDOM from 'react-dom';
import { ActionPiece } from "./types";

interface ActionPieceEditorProps {
    piece: ActionPiece
    onChange: (value: any) => void
}

interface ActionPieceEditorState {

}

class ActionPieceEditor extends React.Component<ActionPieceEditorProps, ActionPieceEditorState> {

    constructor(props: ActionPieceEditorProps) {
        super(props);
    }

    componentDidMount() {
        this.focus();
        // var editor = CodeMirror.fromTextArea(el, {
        //     lineNumbers: true,
        //     lineWrapping: true,
        //     mode: "markdown"
        //   });

    }

    focus() {
        const el = ReactDOM.findDOMNode(this);
        if (el !== null) {
            (el as HTMLElement).focus();
        }
    }

    render() {
        return (
            <textarea onChange={evt => this.props.onChange(evt.target.value)} value={this.props.piece.value}>
            </textarea>
        );
    }
}

export default ActionPieceEditor;