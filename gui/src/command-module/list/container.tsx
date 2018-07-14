import React from 'react';
import ReactDOM from 'react-dom';
import {CommandModuleList, CommandModuleListProps} from './list';

interface CommandModuleListContainerProps extends CommandModuleListProps {

}

class CommandModuleListContainer extends React.Component<CommandModuleListContainerProps, any> {

    componentDidMount() {
    }

    render() {
        return (
            <CommandModuleList {...this.props} />
        );
    }
}

export default CommandModuleListContainer;