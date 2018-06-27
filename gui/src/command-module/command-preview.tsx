import React from 'react';
import { Collapse, Card, CardBody } from "reactstrap";
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { Input } from 'reactstrap'
import Rule from './rule';
import Action from '../action/action';

class CommandPreview extends React.Component<any, any> {

    constructor(params: any) {
        super(params);
        this.state = {
        }
    }

    componentDidMount() {
    }

    render() {
        return (
            <div className="command-preview">
                <Rule text={this.props.rule.text} />
                <Action pieces={this.props.action.pieces} />
            </div>
        );
    }
}

export default CommandPreview;