import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { Table } from 'reactstrap'
import Command from './command';
import {isEqual} from 'lodash'

class CommandModulePanel extends React.Component<any, any> {

    constructor(props: any) {
        super(props);
        this.state = {

        }
    }

    render() {
        const {commands} = this.props.module;
        return (
            <div id="command-module-panel">
                {commands.map((cmd: any, i: Number) =>
                    <Command key={i.toString()} rule={cmd.rule} action={cmd.action} />
                )}
            </div>
        );
    }
}

export default CommandModulePanel;