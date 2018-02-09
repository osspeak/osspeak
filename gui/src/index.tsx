import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { wsFetch } from './websocket';
import {Button} from 'material-ui'
// import "./app.css"
// import CommandModulesView from '../command-modules/view';
// import commandModulesStore from '../command-modules/store';
// import {Provider} from 'mobx-react';
// console.log('rp', Provider);

// const stores = {
//     commandModulesStore
// }

class App extends React.Component<any, {}> {

    componentDidMount() {
    }

    render() {
        return (
            <div id="osspeak-application">
                <Button>foo</Button>
                yarr
                </div>
        );
    }
}

ReactDOM.render(
    <App />,
    document.getElementById('app-root'),
)

// export default App;