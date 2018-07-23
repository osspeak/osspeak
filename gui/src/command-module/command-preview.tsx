import React from 'react';
import { Collapse, Card, CardBody } from "reactstrap";
import ReactDOM from 'react-dom';
import { wsFetch } from '../server';
import { Input } from 'reactstrap'
import Rule from './rule';
import ActionPreview from '../action/action-preview';
import {Command} from './types'

export interface CommandPreviewProps {
    onSelect: any
    command: Command
}

class CommandPreview extends React.Component<any, any> {

    state = {
    }

    constructor(params: any) {
        super(params);
    }

    onSelect = () => {
        this.props.onSelect();
    }

    componentDidMount() {
    }

    render() {
        const { action, rule } = this.props.command
        return (
            <div className="command-preview" onClick={this.onSelect}>
                <Rule text={rule.text} />
                <ActionPreview pieces={action.pieces} />
            </div>
        );
    }
}

export default CommandPreview;