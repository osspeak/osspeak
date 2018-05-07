import React from 'react';
import ReactDOM from 'react-dom';
import CommandModuleListItem from './item';

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