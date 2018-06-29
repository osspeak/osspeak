import React from 'react';
import { Input } from 'reactstrap'

class RuleInput extends React.Component<any, any> {

    constructor(props: any) {
        super(props);
    }

    onModuleSelected = (index: Number) => {
        this.setState({ commandBeingEditedIndex: index })
    }

    toggle = () => {
        this.setState({ commandBeingEditedIndex: null });
    }

    render() {
        // const { commands } = this.props.module;
        return (
            <Input value={this.props.rule.text}>foo</Input>
        );
    }
}

export default RuleInput;