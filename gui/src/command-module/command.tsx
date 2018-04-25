import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { Input } from 'reactstrap'
import Rule from './rule';
import Action from './action';

class Command extends React.Component<any, any> {

    constructor(params: any) {
        super(params);
        this.state = {
        }
    }

    componentDidMount() {
    }

    render() {
        return (
            <div className="command">
                <Rule text={this.props.rule.text} />
                <Action pieces={this.props.action.pieces} />
            </div>
        );
    }
}

export default Command;