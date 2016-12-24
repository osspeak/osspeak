class CommandModuleEditor extends React.Component {

    render() {
        const editorContent = this.props.module.Error ? this.errorContent : this.moduleContent;
        return (
            <div className="editor">
                {editorContent}
            </div>
        );
    }

    changeItem(action, data) {
        data.modulePath = this.props.modulePath;
        this.props.onFieldInput(action, data);
    }


    get moduleContent() {
        const groups = [];
        for (let groupType of ['Rules', 'Functions', 'Commands']) {
            let textObjs = this.props.module[groupType];
            groups.push(<ModuleGroup
                         groupType={groupType}
                         onFieldInput={this.changeItem.bind(this)}
                         textObjs={textObjs}
                         key={groupType}
                        />);
        }
        return groups;
    }

    get errorContent() {
        return this.props.module.Error;
    }
}