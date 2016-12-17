class ModuleGroup extends React.Component {

    changeItem(index, value, fieldKey) {
        const data = {index: index, type: this.props.groupType, value: value, fieldKey: fieldKey};
        this.props.onFieldInput('setItem', data);
    }

    render() {
        const fields = [];
        for (let [index, textObj] of this.props.textObjs.entries()) {
            let fg = <FieldGroup 
                      onFieldInput={this.changeItem.bind(this, index)}
                      type={this.props.groupType}
                      textObj={textObj}
                      textObjKeys={this.props.textObjKeys}
                      key={index}
                     />
            fields.push(fg);
        }
        return (
            <div>
                <h1>{this.props.groupType.toUpperCase()}</h1>
                {fields}
            </div>
        );
    }
}