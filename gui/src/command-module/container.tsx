import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import CommandModulePanel from './panel';
import CommandModuleList from './list';
import {observable} from 'mobx';
import {observer} from 'mobx-react';
import { isEqual } from 'lodash';
import { CommandModuleContainerProps, CommandModuleContainerState } from "./types";

class CommandModuleContainer extends React.Component<CommandModuleContainerProps, CommandModuleContainerState> {

    constructor(props: any) {
        super(props);
        this.state = {
            selectedCommandModule: null,
            activeCommandModules: [],
        }
    }

    get nestedPaths() {
        return Object.keys(this.props.commandModules);
    }

    onListItemClick = (clickedPath: string) => {
        const updatedState: any = { selectedCommandModule: clickedPath }
        const pathOpen = this.state.activeCommandModules.includes(clickedPath);
        if (!pathOpen) updatedState.activeCommandModules = this.state.activeCommandModules.concat([clickedPath])
        this.setState(updatedState);
    }


    componentDidMount() {

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