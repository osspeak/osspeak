import React from 'react';
import { ListGroup, ListGroupItem, Input } from 'reactstrap';
import { ActionPiece } from './types';

interface ActionPieceListProps {
    actionPieces: ActionPiece[]
    onPieceClick: any
}
interface ActionPieceListState {
    selectedPieceIndex: null | number
}

class ActionPieceList extends React.Component<ActionPieceListProps, ActionPieceListState> {

    onClick(index: number) {
        this.setState({ selectedPieceIndex: index });
    }

    constructor(props: ActionPieceListProps) {
        super(props);
        this.state = {
            selectedPieceIndex: null
        }
    }

    actionPiece = (pieceValue: string, index: number) => {
        // if (index === this.state.selectedPieceIndex) {
        //     return <Input key={index} value={pieceValue} onChange={() => null}></Input>
        // }
        return (
            <ListGroupItem
                key={index}
                onClick={() => this.props.onPieceClick(index)}
            >
            {pieceValue}
                {/* <Input key={index} value={pieceValue} onChange={() => null}></Input> */}
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