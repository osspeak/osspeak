import React from 'react';
import { Collapse, Card, CardBody } from "reactstrap";
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { Input } from 'reactstrap'
import Rule from './rule';
import Action from '../action/action';

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
                <Collapse isOpen={this.state.collapse || true}>
                    <Card>
                        <CardBody>
                            Anim pariatur cliche reprehenderit,
                             enim eiusmod high life accusamus terry richardson ad squid. Nihil
                             anim keffiyeh helvetica, craft beer labore wes anderson cred
                             nesciunt sapiente ea proident.
                        </CardBody>
                    </Card>
                </Collapse>
            </div>
        );
    }
}

export default Command;