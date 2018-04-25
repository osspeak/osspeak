import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { Table } from 'reactstrap'
import Command from './command';
import {isEqual} from 'lodash'

class CommandModuleContents extends React.Component<any, any> {

    constructor(props: any) {
        super(props);
        this.state = {
            commands: []
        }
    }

    componentDidMount() {
        this.loadCommandModule();
    }

    componentDidUpdate(prevProps: any) {
        if (!isEqual(prevProps.path, this.props.path)) {
            this.loadCommandModule();
        }
    }

    async loadCommandModule() {
        const commandModule = await wsFetch('COMMAND_MODULE', [this.props.path])
        const { commands } = commandModule;
        this.setState({ commands });
    }

    render() {
        return (
            <div id="command-module-contents">
                {this.props.path}
                {this.state.commands.map((cmd: any, i: Number) =>
                    <Command key={i.toString()} rule={cmd.rule} action={cmd.action} />
                )}
            </div>
        );
    }
}

export default CommandModuleContents;