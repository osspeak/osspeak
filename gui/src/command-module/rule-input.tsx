import React from 'react';
import { Input } from 'reactstrap'
import { Rule } from "./types";

interface RuleInputProps {
    text: string 
}

class RuleInput extends React.Component<RuleInputProps, any> {

    onChange = (evt: any) => {
    }

    render() {
        // const { commands } = this.props.module;
        return (
            <Input value={this.props.text}></Input>
        );
    }
}

export default RuleInput;