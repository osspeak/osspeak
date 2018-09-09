import React from 'react';
import { ListGroup, ListGroupItem } from 'reactstrap';
import { ActionPiece } from './types';

interface ActionPieceListProps {
    actionPieces: ActionPiece[]
}

class ActionPieceList extends React.Component<ActionPieceListProps, any> {

    render() {
        console.log(this.props.actionPieces)

        return (
            <ListGroup>
                {this.props.actionPieces.map((piece, i) =>
                    <ListGroupItem key={i}>{piece.value}</ListGroupItem>
                )}
            </ListGroup>
        );
    }
}

export default ActionPieceList;