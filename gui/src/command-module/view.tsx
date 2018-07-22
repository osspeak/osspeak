import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../server';
import CommandModulePanel from './panel';
import CommandModuleContainer from './container';
import CommandModuleTabs from './tabs';
import CommandModuleList from './list/container';
import { isEqual } from 'lodash';
import { RecognitionIndex, CommandModule } from "./types";

export interface CommandModuleContainerProps {
    recognitionIndex: RecognitionIndex
}

export interface CommandModuleContainerState {
    focusedPath: null | string
    selectedPaths: string[]
}


class CommandModuleView extends React.Component<CommandModuleContainerProps, CommandModuleContainerState> {

    state: CommandModuleContainerState = {
        focusedPath: null,
        selectedPaths: [],
    }

    constructor(props: any) {
        super(props);
    }

    onTabClick = (name: string) => {
        this.setState({ focusedPath: name });
    }

    get nestedPaths() {
        return Object.keys(this.props.recognitionIndex.commandModules);
    }

    onListItemClick = (clickedPath: string) => {
        // const updatedState: Partial<CommandModuleContainerState> = { selectedPath: clickedPath }
        const updatedState: any = { focusedPath: clickedPath }
        const pathOpen = this.state.selectedPaths.includes(clickedPath);
        if (!pathOpen) updatedState.selectedPaths = this.state.selectedPaths.concat([clickedPath])
        this.setState(updatedState);
    }


    componentDidMount() {

    }

    render() {
        const { commandModules, activeCommandModules } = this.props.recognitionIndex;
        let focusedCommandModule: CommandModule | null = null;
        if (this.state.focusedPath !== null) {
            focusedCommandModule = {
                path: this.state.focusedPath,
                config: commandModules[this.state.focusedPath]
            }
        }
        return (
            <div id="cm-container">
                <CommandModuleList
                    onListItemClick={this.onListItemClick}
                    paths={this.nestedPaths}
                    activePaths={new Set(activeCommandModules)}
                />
                {this.state.focusedPath && (
                    <div id="command-module-contents">
                        <CommandModuleTabs
                            focused={this.state.focusedPath}
                            onTabClick={this.onTabClick}
                            paths={this.state.selectedPaths}
                        />
                        {focusedCommandModule !== null && <CommandModuleContainer commandModule={focusedCommandModule} />}
                    </div>
                )}
            </div>
        );
    }
}

export default CommandModuleView;