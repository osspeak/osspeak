import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { Button } from 'material-ui'
import CommandModulePanel from './panel';
import CommandModuleList from './list';
import {observable} from 'mobx';
import {observer} from 'mobx-react';
import { isEqual } from 'lodash';
import {CommandModuleStore, store} from './store';

@observer class CommandModuleContainer extends React.Component<any, any> {

    store: CommandModuleStore

    constructor(props: any) {
        super(props);
        this.store = store;
        this.state = {
            paths: [],
            selectedCommandModule: null,
            activeCommandModules: [],
        }
    }

    get nestedPaths() {
        return this.state.paths
    }

    onListItemClick = (clickedPath: [string]) => {
        const updatedState: any = { selectedCommandModule: clickedPath };
        let pathOpen = false;
        for (const path of this.state.activeCommandModules) {
            if (isEqual(path, clickedPath)) {
                pathOpen = true;
                break;
            };
        }
        if (!pathOpen) updatedState.activeCommandModules = this.state.activeCommandModules.concat([clickedPath])
        this.setState(updatedState);
    }


    componentDidMount() {
        this.loadCommandModules();
    }

    async loadCommandModules() {
        const commandModules = await wsFetch('COMMAND_MODULES');
        this.setState({ paths: commandModules.paths })
    }

    render() {
        return (
            <div id="cm-container">
                <CommandModuleList onListItemClick={this.onListItemClick} paths={this.nestedPaths} />
                {this.state.selectedCommandModule && <CommandModulePanel
                    path={this.state.selectedCommandModule}
                    commandModules={this.state.activeCommandModules}
                />}
                {this.state.activeCommandModules}
            </div>
        );
    }
}

export default CommandModuleContainer;