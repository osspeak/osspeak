class CommandModuleEditor extends React.Component {

    render() {
        const groups = [];
        for (var groupType of ['Rules', 'Functions', 'Commands']) {
            let textObjs = this.props.module[groupType];
            groups.push(<ModuleGroup
                         groupType={groupType}
                         onFieldInput={this.changeItem.bind(this)}
                         textObjs={textObjs}
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
        data.modulePath = this.props.modulePath;
        this.props.onFieldInput(action, data);
    }

}