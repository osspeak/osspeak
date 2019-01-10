import { Nav, NavItem, NavLink } from "reactstrap";
import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../server';
import { } from "./types";
import classnames from 'classnames';

export interface CommandModuleTabsProps {
    focused: string
    onTabClick: (name: string) => void
    paths: string[]
}
export interface CommandModuleTabsState {

}

class CommandModuleTabs extends React.Component<CommandModuleTabsProps, CommandModuleTabsState> {

    componentDidMount() {
    }

    render() {
        return (
            <div id="command-module-tabs">
                <Nav tabs>
                    {this.props.paths.map((path) => (
                        <NavItem key={path}>
                            <NavLink
                                className={classnames({ active: this.props.focused === path })}
                                onClick={() => this.props.onTabClick(path)}
                            >
                                {path}
                            </NavLink>
                        </NavItem>
                    ))
                    }
                </Nav>
            </div>
        );
    }
}

export default CommandModuleTabs;