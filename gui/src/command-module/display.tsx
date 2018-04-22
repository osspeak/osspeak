import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { Button } from 'material-ui'
import { Treebeard } from 'react-treebeard';

class  CommandModuleDisplay extends React.Component<any, {}> {

    componentDidMount() {
    }

    render() {
        return (
            <div id="osspeak-application">
                cm
            </div>
        );
    }
}

export default CommandModuleDisplay;