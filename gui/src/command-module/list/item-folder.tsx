import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../../websocket';

class CommandModuleListItemFolder extends React.Component<any, {}> {

    componentDidMount() {
    }

    render() {
        return (
            <div className="cm-list-item" onClick={() => this.props.onClick(this.props.value)}>
                {this.props.value}
            </div>
        );
    }
}

export default CommandModuleListItemFolder;