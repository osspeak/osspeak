class CommandModuleEditor extends React.Component {

    constructor(props, context) {
        super(props, context);
    }

    render() {
        return (
            <div className="editor">
                <ModuleGroup title='Variables' textObjs={this.props.module.variables} />
                <ModuleGroup title='Functions' textObjs={this.props.module.functions} />
                <ModuleGroup title='Commands' textObjs={this.props.module.commands} /> 
            </div>
        );
    }
    
}