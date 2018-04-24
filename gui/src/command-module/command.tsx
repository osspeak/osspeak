import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { Table } from 'reactstrap'

class Command extends React.Component<any, any> {

    constructor(params: any) {
        super(params);
        this.state = {
            commands: []
        }
    }

    componentDidMount() {
    }

    render() {
        return (
            <div>
                {this.props.rule.text}
            </div>
        );
    }
}

export default Command;