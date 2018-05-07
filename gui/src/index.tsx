import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import ReactDOM from 'react-dom';
import { createStore, } from "redux";
import { Provider } from "react-redux";
import { ws, wsFetch } from './websocket';
import { Button } from 'material-ui'
import { Treebeard } from 'react-treebeard';
import './command-module/command-module.css';
import CommandModuleContainer from './command-module/container';

class App extends React.Component<any, any> {

    constructor(props: any) {
        super(props);
        this.state = {
            commandModules: {}
        }
    }

    componentDidMount() {
        this.loadIndex();
    }

    async loadIndex() {
        const {commandModules} = await wsFetch('COMMAND_MODULE_INDEX');
        this.setState({commandModules});
    }
    
    render() {
        return (
            <div id="osspeak-application">
                <CommandModuleContainer commandModules={this.state.commandModules} />
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