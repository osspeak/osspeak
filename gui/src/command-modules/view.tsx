import * as React from 'react';
import * as ReactDOM from 'react-dom';
import {observable} from 'mobx'
import {observer, inject} from "mobx-react";
import './command-modules.css';

@inject('commandModulesStore') @observer
class CommandModulesViewContainer extends React.Component<any, any> {

    componentDidMount() {
        this.props.commandModulesStore.fetchCommandModuleTree();
    }
    
    render() {
        return (
            <div id="command-modules-view">
                
            </div>
        );
    }
}

export default CommandModulesViewContainer;