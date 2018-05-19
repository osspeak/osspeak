import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import CommandModulePanel from './panel';
import CommandModuleTabs from './tabs';
import CommandModuleList from './list/list';
import { observable } from 'mobx';
import { observer } from 'mobx-react';
import { isEqual } from 'lodash';
import { CommandModuleContainerProps, CommandModuleContainerState } from "./types";

class CommandModuleContainer extends React.Component<CommandModuleContainerProps, CommandModuleContainerState> {

    constructor(props: any) {
        super(props);
        this.state = {
            selectedPath: null,
            activePaths: [],
        }
    }

    get nestedPaths() {
        return Object.keys(this.props.commandModules);
    }

    onListItemClick = (clickedPath: string) => {
        // const updatedState: Partial<CommandModuleContainerState> = { selectedPath: clickedPath }
        const updatedState: any = { selectedPath: clickedPath }
        const pathOpen = this.state.activePaths.includes(clickedPath);
        if (!pathOpen) updatedState.activePaths = this.state.activePaths.concat([clickedPath])
        this.setState(updatedState);
    }


    componentDidMount() {

    }

    render() {
        return (
            <div id="cm-container">
                <CommandModuleList onListItemClick={this.onListItemClick} paths={this.nestedPaths} />
                {this.state.selectedPath && (
                    <div id="command-module-contents">
                        <CommandModuleTabs paths={this.state.activePaths} />
                        <CommandModulePanel module={this.props.commandModules[this.state.selectedPath]} />
                    </div>
                )}
                {this.state.activePaths}
            </div>
        );
    }
}

export default CommandModuleContainer;