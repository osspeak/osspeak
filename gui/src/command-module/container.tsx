import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { Button } from 'material-ui'
import CommandModule from './command-module';
import CommandModuleList from './list';
import { Treebeard } from 'react-treebeard';

class CommandModuleContainer extends React.Component<any, {}> {

    componentDidMount() {
    }

    render() {
        return (
            <div id="cm-container">
                                <CommandModuleList />
                <CommandModule />

            </div>
        );
    }
}

export default CommandModuleContainer;