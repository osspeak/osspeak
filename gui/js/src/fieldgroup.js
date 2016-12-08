class FieldGroup extends React.Component {
    render() {
        const textArr = this.textArr;
        return (
            <div className="hbox">
                <input className="form-control editor-input" type="text" defaultValue={textArr[0]} />
                <input className="form-control editor-input" type="text" defaultValue={textArr[1]} />
            </div>
        );
    }

    get textArr() {
        const arr = [];
        arr.push(this.firstText());
        arr.push(this.secondText());
        return arr;
    }

    firstText() {
        if (this.props.type === 'variables') return this.props.textObj.name;
        if (this.props.type === 'functions') return this.props.textObj.signature;
        if (this.props.type === 'commands') return this.props.textObj.rule.text;
    }

    secondText() {
        if (this.props.type === 'variables') return this.props.textObj['rule_text'];
        if (this.props.type === 'functions') return this.props.textObj.action;
        if (this.props.type === 'commands') return this.props.textObj.action.text;
    }

}