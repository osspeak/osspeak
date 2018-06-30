import React from 'react';
import ReactDOM from 'react-dom';


// import * as monaco from 'monaco-editor';


class ActionPieceEditor extends React.Component<any, any> {

    constructor(props: any) {
        super(props);
    }

    componentDidMount() {
        // var editor = CodeMirror.fromTextArea(el, {
        //     lineNumbers: true,
        //     lineWrapping: true,
        //     mode: "markdown"
        //   });
          
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
            // <textarea style={{height: '200px', width: '200px'}}>
            <textarea >
            </textarea>
        );
    }
}

export default ActionPieceEditor;