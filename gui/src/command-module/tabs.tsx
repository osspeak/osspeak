import { Nav, NavItem, NavLink } from "reactstrap";
import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { CommandModuleTabsProps } from "./types";
import classnames from 'classnames';

class CommandModuleTabs extends React.Component<CommandModuleTabsProps, {}> {

    componentDidMount() {
    }

    render() {
        console.log(this.props.paths)
        return (
            <div id="command-module-tabs">
                <Nav tabs>
                    {this.props.paths.map((path) => (
                        <NavItem key={path}>
                            <NavLink
                                className={classnames({ active: this.props.selected === path })}
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