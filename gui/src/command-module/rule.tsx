import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../server';
import { Input } from 'reactstrap'

class Rule extends React.Component<any, any> {

    render() {
        return (
            <div className="rule-input">
                {this.props.text}
            </div>
        );
    }
}

export default Rule;