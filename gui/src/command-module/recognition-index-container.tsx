import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch, ServerSubscription, subscribe } from '../server';
import CommandModulePanel from './panel';
import CommandModuleContainer from './command-module-container';
import AppView from './app-view';
import CommandModuleTabs from './tabs';
import CommandModuleList from './list/container';
import { isEqual } from 'lodash';
import { RecognitionIndex, CommandModule } from "./types";
const Ajv = require('ajv');
declare var window: any
const VALIDATE = new Ajv().compile(JSON.parse(window.commandLineArgs.jsonModuleSchema))
console.log(VALIDATE)
export interface RecognitionIndexContainerProps {

}

export interface RecognitionIndexContainerState {
    recognitionIndex: RecognitionIndex | null
}


class RecognitionIndexContainer extends React.Component<RecognitionIndexContainerProps, RecognitionIndexContainerState> {

    indexSubscription: ServerSubscription | null

    componentDidMount() {
        this.indexSubscription = subscribe('RECOGNITION_INDEX',
            (index: RecognitionIndex) => this.setState({ recognitionIndex: index }));
        this.loadIndex();
    }

    async loadIndex() {
        const recognitionIndex = await wsFetch('RECOGNITION_INDEX');
        console.log('ri', recognitionIndex)
        this.validateCommandModules(recognitionIndex);
        this.setState({ recognitionIndex });
    }

    validateCommandModules(index: RecognitionIndex) {
        for (const [path, commandModule] of Object.entries(index.commandModules)) {
            console.log(VALIDATE(commandModule));
            
        }
    }

    constructor(props: RecognitionIndexContainerProps) {
        super(props);
        this.indexSubscription = null;
        this.state = {
            recognitionIndex: null
        }
    }

    render() {
        return (
            <div id="cm-container">
                {this.state.recognitionIndex !== null && <AppView recognitionIndex={this.state.recognitionIndex} />}
            </div>
        );
    }
}

export default RecognitionIndexContainer;