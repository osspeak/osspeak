import React from 'react';
import { Input } from 'reactstrap'
import { Rule } from "./types";

interface RuleInputProps {
    text: string
    onChange: any
}

class RuleInput extends React.Component<RuleInputProps, any> {

    onChange = (evt: any) => {
    }

    render() {
        // const { commands } = this.props.module;
        return (
            <Input
                onChange={(evt: any) => this.props.onChange(evt.target.value)}
                value={this.props.text}>
            </Input>
        );
    }
}

export default RuleInput;