import * as React from 'react';
import * as ReactDOM from 'react-dom';
import "./app.css"

class App extends React.Component<{}, {}> {
    render() {
        return (
            <div id="osspeak-application">
                yar
            </div>
        );
    }
}

ReactDOM.render(
    <App />,
    document.getElementById('app-root'),
)

export default App;