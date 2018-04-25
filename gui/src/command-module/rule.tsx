import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { Input } from 'reactstrap'

class Rule extends React.Component<any, any> {

    render() {
        return (
            <Input value={this.props.text} />
        );
    }
}

export default Rule;