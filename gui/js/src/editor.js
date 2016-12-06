class CommandModuleEditor extends React.Component {

    constructor(props, context) {
        super(props, context);
    }

    render() {
        return (
            <div className="editor">
                <ModuleGroup title='Variables' />
                <ModuleGroup title='Functions' />
                <ModuleGroup title='Commands' /> 
            </div>
        );
    }
    
}