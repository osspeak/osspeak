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
        console.log('cml', this.props)
        return (
            <div>
                {this.props.paths.map((path: string) => {
                    return <CommandModuleListItem key={path} onClick={this.props.onListItemClick} value={path} />
                })}
            </div>
        );
    }
}

export default CommandModuleList;