import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from './websocket';
import { Button } from 'material-ui'
import { Treebeard } from 'react-treebeard';
import './command-module/command-module.css';
import CommandModuleContainer from './command-module/container';
// import "./app.css"
// import CommandModulesView from '../command-modules/view';
// import commandModulesStore from '../command-modules/store';
// import {Provider} from 'mobx-react';
// console.log('rp', Provider);

// const stores = {
//     commandModulesStore
// }

console.log(wsFetch)

class App extends React.Component<any, {}> {

    componentDidMount() {
    }

    render() {
        return (
            <div id="osspeak-application">
                <Button>foo</Button>
                <CommandModuleContainer />
                {/* <TreeExample /> */}
            </div>
        );
    }
}

ReactDOM.render(
    <App />,
    document.getElementById('app-root'),
)

// export default App;