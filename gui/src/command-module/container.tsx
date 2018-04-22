import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { Button } from 'material-ui'
import CommandModuleDisplay from './display';
import CommandModuleList from './list';
// import {observer} from 'react-mobx';
import { Treebeard } from 'react-treebeard';
import { commandModuleStore, CommandModuleStore } from './store'
import {isEqual} from 'lodash';

class CommandModuleContainer extends React.Component<any, any> {

    // store: CommandModuleStore

    get nestedPaths() {
        return this.state.paths
    }

    onListItemClick = (clickedPath: [string]) => {
        const updatedState: any = {selectedCommandModule: clickedPath};
        let pathOpen = false;
        for (const path of this.state.activeCommandModules) {
            if (isEqual(path, clickedPath)) {
                pathOpen = true;
                break;   
            };
        }
        if (!pathOpen) updatedState.activeCommandModules = this.state.activeCommandModules.concat([clickedPath])
        console.log('olic', clickedPath, updatedState)
        this.setState(updatedState);
    }

    constructor(params: any) {
        super(params);
        this.state = {
            paths: [],
            selectedCommandModule: null,
            activeCommandModules: [],
        }
        // this.store = commandModuleStore;
    }

    componentDidMount() {
        this.loadCommandModules();
    }

    async loadCommandModules() {
        const commandModules = await wsFetch('COMMAND_MODULES');
        this.setState({paths: commandModules.paths})
        console.log(commandModules);
    }

    render() {
        return (
            <div id="cm-container">
                <CommandModuleList onListItemClick={this.onListItemClick} paths={this.nestedPaths} />
                <CommandModuleDisplay commandModules={this.state.activeCommandModules} />
                {this.state.activeCommandModules}
            </div>
        );
    }
}

export default CommandModuleContainer;