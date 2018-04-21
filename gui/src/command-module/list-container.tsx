import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { Button } from 'material-ui'
import CommandModuleList from './list';

class CommandModuleListContainer extends React.Component<any, {}> {

    componentDidMount() {
    }

    render() {
        return (
            <CommandModuleList />
        );
    }
}

export default CommandModuleListContainer;