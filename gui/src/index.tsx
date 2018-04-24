import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from './websocket';
import { Button } from 'material-ui'
import { Treebeard } from 'react-treebeard';
import './command-module/command-module.css';
import { ws } from './websocket';
import CommandModuleContainer from './command-module/container';

class App extends React.Component<any, {}> {

    componentDidMount() {
    }

    render() {
        return (
            <div id="osspeak-application">
                <CommandModuleContainer />
                {/* <TreeExample /> */}
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