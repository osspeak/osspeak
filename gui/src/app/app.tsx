import * as React from 'react';
import * as ReactDOM from 'react-dom';
import "./app.css"
import CommandModulesView from '../command-modules/view';
import {wsFetch} from '../websocket';
wsFetch

class App extends React.Component<{}, {}> {

    componentDidMount() {
        // console.log(ws)
    }

    render() {
        return (
            <div id="osspeak-application">
                yarr
                <CommandModulesView />
            </div>
        );
    }
}

ReactDOM.render(
    <App />,
    document.getElementById('app-root'),
)

export default App;