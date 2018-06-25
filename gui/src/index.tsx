import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import ReactDOM from 'react-dom';
import { createStore, } from "redux";
import { Provider } from "react-redux";
import { ws, wsFetch } from './websocket';
import { Button } from 'material-ui'
import { Treebeard } from 'react-treebeard';
import { AppState } from "./types";
import './command-module/command-module.css';
import CommandModuleContainer from './command-module/container';

class App extends React.Component<any, AppState> {

    constructor(props: any) {
        super(props);
        this.state = {
            recognitionIndex: {}
        }
    }

    componentDidMount() {
        this.loadIndex();
    }

    async loadIndex() {
        const {recognitionIndex} = await wsFetch('RECOGNITION_INDEX');
        this.setState({recognitionIndex});
    }
    
    render() {
        return (
            <div id="osspeak-application">
                <CommandModuleContainer recognitionIndex={this.state.recognitionIndex} />
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