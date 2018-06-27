import React from 'react';
import { Collapse, Card, CardBody } from "reactstrap";
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { Input } from 'reactstrap'
import CommandHeader from './command-header';
import Rule from './rule';
import ActionPreview from '../action/action-preview';

class CommandPreview extends React.Component<any, any> {

    constructor(params: any) {
        super(params);
        this.state = {
        }
    }

    componentDidMount() {
    }

    render() {
        const { action, rule } = this.props.command
        return (
            <div className="command-preview">
                <Rule text={rule.text} />
                <ActionPreview pieces={action.pieces} />
            </div>
        );
    }
}

export default CommandPreview;