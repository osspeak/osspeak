import React from 'react';
import ReactDOM from 'react-dom';
import { ActionPiece } from "./types";

interface ActionPieceEditorProps {
    piece: ActionPiece
    onChange: (value: any) => void
}

class ActionPieceEditor extends React.Component<ActionPieceEditorProps, any> {

    constructor(props: ActionPieceEditorProps) {
        super(props);
    }

    componentDidMount() {
        console.log('tp', this.props.piece)
        // var editor = CodeMirror.fromTextArea(el, {
        //     lineNumbers: true,
        //     lineWrapping: true,
        //     mode: "markdown"
        //   });

    }

    onModuleSelected = (index: number) => {
        this.setState({ commandBeingEditedIndex: index })
    }

    toggle = () => {
        this.setState({ commandBeingEditedIndex: null });
    }

    render() {
        // const { commands } = this.props.module;
        return (
            // <textarea style={{height: '200px', width: '200px'}}>
            <textarea onChange={evt => this.props.onChange(evt.target.value)} value={this.props.piece.value}>
            </textarea>
        );
    }
}

export default ActionPieceEditor;