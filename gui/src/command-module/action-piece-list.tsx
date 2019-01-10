import React from 'react';
import { ListGroup, ListGroupItem, Input } from 'reactstrap';
import { ActionPiece } from './types';

interface ActionPieceListProps {
    actionPieces: ActionPiece[]
    onPieceClick: any
    selectedIndex: null | number
}
interface ActionPieceListState {
}

class ActionPieceList extends React.Component<ActionPieceListProps, ActionPieceListState> {

    onClick(index: number) {
    }

    constructor(props: ActionPieceListProps) {
        super(props);
    }

    actionPiece = (pieceValue: string, index: number) => {
        const isActive = index === this.props.selectedIndex;
        return (
            <ListGroupItem
                active={isActive}
                key={index}
                onClick={() => this.props.onPieceClick(index)}
            >
                {pieceValue}
            </ListGroupItem>
        )
    }

    render() {
        return (
            <ListGroup>
                {this.props.actionPieces.map((piece, i) => this.actionPiece(piece.value, i))}
            </ListGroup>
        );
    }
}

export default ActionPieceList;