import React from 'react';
import ReactDOM from 'react-dom';
import CommandModuleListItem from './item';

interface CommandModuleListProps {
    paths: string[]
    activePaths: Set<string>
    onListItemClick: any
}

class CommandModuleList extends React.Component<CommandModuleListProps, null> {
    
    

    componentDidMount() {
    }
    
    render() {
        console.log('tp', this.props.activePaths)
        return (
            <div>
                {this.props.paths.map((path: string, i: any) => {
                    const focused = this.props.activePaths.has(path)
                    return <CommandModuleListItem key={i} focused={focused} onClick={this.props.onListItemClick} value={path} />
                })}
            </div>
        );
    }
}

export default CommandModuleList;