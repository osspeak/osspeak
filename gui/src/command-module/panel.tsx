import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { Table } from 'reactstrap'
import CommandPreview from './command-preview';
import { CommandModulePanelProps } from "./types";

class CommandModulePanel extends React.Component<any, any> {

    constructor(props: any) {
        super(props);
        this.state = {
            commandBeingEditedIndex: null,
        }
    }

    render() {
        const {commands} = this.props.module;
        return (
            <div id="command-module-panel">
                {commands.map((cmd: any, i: Number) =>
                    <CommandPreview key={i.toString()} command={cmd} />
                )}
            </div>
        );
    }
}

export default CommandModulePanel;