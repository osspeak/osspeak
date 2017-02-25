class ModuleGroup extends React.Component {

    changeItem(index, value, fieldKey) {
        const data = {index: index, type: this.props.groupType, value: value, fieldKey: fieldKey};
        this.props.onFieldInput('setItem', data);
    }

    render() {
        const fields = [];
        const fieldObjects = this.fieldGroupObjects;
        for (let [index, textObj] of fieldObjects.entries()) {
            let fg = <FieldGroup 
                      onFieldInput={this.changeItem.bind(this, index)}
                      type={this.props.groupType}
                      textObj={textObj}
                      key={index}
                     />
            fields.push(fg);
        }
        const title = this.props.groupType[0].toUpperCase() + this.props.groupType.substring(1, this.props.groupType.length);
        return (
            <div>
                <h3>{title}</h3>
                {fields}
            </div>
        );
    }

    get fieldGroupObjects() {
        const textObjs = Array.isArray(this.props.textObjs) ? this.props.textObjs : [];
        const groupObjects = [];
        for (let textObj of textObjs) {
            groupObjects.push(this.getTextTypes(textObj));
        }
        return groupObjects;
    }

    getTextTypes(textObj) {
        switch (this.props.groupType) {
            case 'rules':
                return [textObj.name, textObj.value];
            case 'functions':
                return [textObj.signature, textObj.action];
            case 'commands':
                return [textObj.rule.value, textObj.action];
        }
    }

}