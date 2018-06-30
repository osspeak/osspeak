import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { ModalHeader, ModalBody, ModalFooter, Button } from 'reactstrap'
import ActionList from './action-list';
import RuleInput from './rule-input';
import { CommandModulePanelProps } from "./types";

declare var CodeMirror: any

// import * as monaco from 'monaco-editor';


class ActionEditor extends React.Component<any, any> {

    constructor(props: any) {
        super(props);
    }

    componentDidMount() {
        const el = ReactDOM.findDOMNode(this) as HTMLDivElement;
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

export default ActionEditor;