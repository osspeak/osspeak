import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';

class CommandModuleContents extends React.Component<any, {}> {

    componentDidMount() {
        this.loadCommandModule();
    }

    async loadCommandModule() {
        console.log(this.props);
        const commandModule = await wsFetch('COMMAND_MODULE', [this.props.path])
        console.log(commandModule);
    }

    render() {
        return (
            <div id="command-module-contents">
                {this.props.path}
            </div>
        );
    }
}

export default CommandModuleContents;