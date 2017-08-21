import * as React from 'react';
import * as ReactDOM from 'react-dom';
import "./app.css"
import CommandModulesView from '../command-modules/view';
import commandModulesStore from '../command-modules/store';
import {wsFetch} from '../websocket';
import {Provider} from 'mobx-react';
wsFetch
console.log('rp', Provider);

const stores = {
    commandModulesStore
}

class App extends React.Component<any, {}> {

    componentDidMount() {
        // console.log(ws)
        console.log(this, this.props);
    }

    render() {
        return (
            <Provider {...this.props.stores}>
                <div id="osspeak-application">
                    yarr
                    <CommandModulesView />
                </div>
            </Provider>
        );
    }
}

ReactDOM.render(
    <App stores={stores} />,
    document.getElementById('app-root'),
)

export default App;