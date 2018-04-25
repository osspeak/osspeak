import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { Button } from 'material-ui'
import { Treebeard } from 'react-treebeard';
import CommandModuleListItem from './list-item';

class CommandModuleList extends React.Component<any, {}> {

    componentDidMount() {
    }
    
    render() {
        return (
            <div>
                {this.props.paths.map((path: string, i: any) => {
                    return <CommandModuleListItem key={i} onClick={this.props.onListItemClick} value={path} />
                })}
            </div>
        );
    }
}

export default CommandModuleList;