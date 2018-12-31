import React from 'react';
import ReactDOM from 'react-dom';
import { ActionPiece } from "./types";

interface ActionPieceEditorProps {
    piece: ActionPiece
}

class ActionPieceEditor extends React.Component<any, any> {

    constructor(props: any) {
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
            <textarea >
                
            </textarea>
        );
    }
}

export default ActionPieceEditor;