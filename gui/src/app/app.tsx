import * as React from 'react';
import * as ReactDOM from 'react-dom';
import "./app.css"
import CommandModulesView from '../command-modules/view';
import {pollServer} from '../poll'

console.log('nit')
class App extends React.Component<{}, {}> {

    componentDidMount() {
        pollServer();
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