class CommandModuleEditor extends React.Component {

    constructor(props, context) {
        super(props, context);
        this.textObjKeys = {
            variables: ['name', 'rule_text'],
            functions: ['signature', 'action'],
            commands: ['rule.text', 'action.text'],
        }
    }

    render() {
        const groups = [];
        for (var groupType of ['variables', 'functions', 'commands']) {
            let textObjs = this.props.module[groupType];
            let textObjKeys = this.textObjKeys[groupType];
            groups.push(<ModuleGroup
                         groupType={groupType}
                         onFieldInput={this.changeItem.bind(this)}
                         textObjs={textObjs}
                         textObjKeys={textObjKeys}
                         key={groupType}
                        />);
        }
        return (
            <div className="editor">
                {groups}
            </div>
        );
    }

    changeItem(action, data) {
        data.modulePath = this.props.module.path;
        this.props.onFieldInput(action, data);
    }

}