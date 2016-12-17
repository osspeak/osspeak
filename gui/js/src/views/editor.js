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
                         onFieldInput={this.props.onFieldInput}
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

    firstName(type) {
        if (type === 'variables') return 'name';
        if (type === 'functions') return 'signature';
        if (type === 'commands') return 'rule.text';
    }

    secondName(type) {
        if (type === 'variables') return 'rule_text';
        if (type === 'functions') return 'action';
        if (type === 'commands') return 'action.text';
    }
    
}