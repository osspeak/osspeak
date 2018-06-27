import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { Input } from 'reactstrap'
import { ActionProps } from "./types";

class ActionPreview extends React.Component<ActionProps, any> {

    render() {
        return (
            <div className="action-preview">
                {this.props.pieces.map((piece) => {
                    return <div>{piece.value}</div>
                })}
            </div>
        );
    }
}

export default ActionPreview;