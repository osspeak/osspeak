console.log('test')
import * as React from 'react';
import * as ReactDOM from 'react-dom';
// import "./app.css"
// import CommandModulesView from '../command-modules/view';
// import commandModulesStore from '../command-modules/store';
// import {wsFetch} from '../websocket';
// import {Provider} from 'mobx-react';
// console.log('rp', Provider);

// const stores = {
//     commandModulesStore
// }

class App extends React.Component<any, {}> {

    componentDidMount() {
        // console.log(ws)
        console.log(this, this.props);
    }

    render() {
        return (
                <div id="osspeak-application">
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