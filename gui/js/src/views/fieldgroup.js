class FieldGroup extends React.Component {

    render() {
        const textArr = this.textArr;
        return (
            <div className="hbox">
                <InputField keyName={textArr[0].key} value={textArr[0].value} onInput={this.props.onFieldInput} />
                <i className="fa fa-long-arrow-right"></i>
                <InputField keyName={textArr[1].key} value={textArr[1].value} onInput={this.props.onFieldInput} />
            </div>
        );
    }

    get textArr() {
        const arr = [];
        for (let i = 0; i < 2; i++) {
            let fieldKey = this.props.textObjKeys[i];
            let fieldValue = this.getTextObjProp(fieldKey);
            arr.push({key: fieldKey, value: fieldValue});
        }
        return arr;
    }

    getTextObjProp(accessorStr) {
        let prop = this.props.textObj;
        for (let accessorPiece of accessorStr.split('.')) {
            prop = prop[accessorPiece];
        }
        return prop;
    }

}