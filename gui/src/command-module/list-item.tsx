import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { Button } from 'material-ui'
import { Treebeard } from 'react-treebeard';

class CommandModuleListItem extends React.Component<any, {}> {

    componentDidMount() {
    }

    render() {
        return (
            <div className="cm-list-item" onClick={() => this.props.onClick(this.props.value)}>
                foo
                {this.props.value}
            </div>
        );
    }
}

export default CommandModuleListItem;