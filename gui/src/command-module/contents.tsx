import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { Table } from 'reactstrap'
import Command from './command';

class CommandModuleContents extends React.Component<any, any> {

    constructor(params: any) {
        super(params);
        this.state = {
            commands: []
        }
    }

    componentDidMount() {
        this.loadCommandModule();
    }

    async loadCommandModule() {
        console.log(this.props);
        const commandModule = await wsFetch('COMMAND_MODULE', [this.props.path])
        const { commands } = commandModule;
        this.setState({ commands });
        console.log(commandModule);
    }

    render() {
        return (
            <div id="command-module-contents">
                {this.props.path}
                {this.state.commands.map((cmd: any, i: Number) =>
                    <Command key={i.toString()} rule={cmd.rule} />
                )}
            </div>
        );
    }
}

export default CommandModuleContents;