import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../server';
import { Input } from 'reactstrap'

class ActionPreview extends React.Component<any, any> {

    render() {
        return (
            <div className="action-preview">
                {this.props.pieces.map((piece: any, i: number) => {
                    return <div key={i}>{piece.value}</div>
                })}
            </div>
        );
    }
}

export default ActionPreview;