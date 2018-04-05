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

const data = {
    name: 'root',
    toggled: true,
    children: [
        {
            name: 'parent',
            children: [
                { name: 'child1' },
                { name: 'child2' }
            ]
        },
        {
            name: 'loading parent',
            loading: true,
            children: []
        },
        {
            name: 'parent',
            children: [
                {
                    name: 'nested parent',
                    children: [
                        { name: 'nested child 1' },
                        { name: 'nested child 2' }
                    ]
                }
            ]
        }
    ]
};

class TreeExample extends React.Component<any, any> {
    constructor(props: any) {
        super(props);
        this.state = {};
        this.onToggle = this.onToggle.bind(this);
    }
    onToggle(node: any, toggled: any) {
        if (this.state.cursor) { this.state.cursor.active = false; }
        node.active = true;
        if (node.children) { node.toggled = toggled; }
        this.setState({ cursor: node });
    }
    render() {
        return (
            <Treebeard
                data={data}
                onToggle={this.onToggle}
            />
        );
    }
}

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