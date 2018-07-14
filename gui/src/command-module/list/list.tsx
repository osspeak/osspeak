import React from 'react';
import ReactDOM from 'react-dom';
import CommandModuleListItem from './item';

export interface CommandModuleListProps {
    paths: string[]
    activePaths: Set<string>
    onListItemClick: any
}

export class CommandModuleList extends React.Component<CommandModuleListProps, any> {

    componentDidMount() {
    }
    
    render() {
        return (
            <div>
                {this.props.paths.map((path: string, i: any) => {
                    const focused = this.props.activePaths.has(path)
                    return <CommandModuleListItem
                        key={i}
                        focused={focused}
                        onClick={this.props.onListItemClick}
                        value={path}
                    />
                })}
            </div>
        );
    }
}