import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import ReactDOM from 'react-dom';
import { ws, wsFetch, subscribe, ServerSubscription } from './server';
import { RecognitionIndex } from "./command-module/types";
import './command-module/command-module.css';
import './action/action.css';
import CommandModuleView from './command-module/view';

export interface AppState {
    recognitionIndex: RecognitionIndex | null
}

class App extends React.Component<any, AppState> {

    indexSubscription: ServerSubscription | null

    state: AppState = {
        recognitionIndex: null
    }

    constructor(props: any) {
        super(props);
        this.indexSubscription = null;
    }

    componentDidMount() {
        this.indexSubscription = subscribe('RECOGNITION_INDEX',
            (index: RecognitionIndex) => this.setState({recognitionIndex: index}));
        this.loadIndex();
    }

    async loadIndex() {
        const recognitionIndex = await wsFetch('RECOGNITION_INDEX');
        this.setState({recognitionIndex});
    }
    
    render() {
        return (
            <div id="osspeak-application">
                {this.state.recognitionIndex !== null && <CommandModuleView
                    recognitionIndex={this.state.recognitionIndex}
                />}
            </div>
        );
    }
}

ws.onopen = () => {
    ReactDOM.render(
        <App />,
        document.getElementById('app-root'),
    )
}

// export default App;