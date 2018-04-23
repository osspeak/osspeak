import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';

import CommandModuleContents from './contents';
import CommandModuleTabs from './tabs';

class CommandModulePanel extends React.Component<any, {}> {

    componentDidMount() {
    }

    render() {
        return (
            <div id="command-module-panel">
                <CommandModuleTabs paths={this.props.commandModules} />
                <CommandModuleContents path={this.props.path} />
           </div>
        );
    }
}

export default CommandModulePanel;