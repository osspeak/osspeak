class EditorTabPanel extends React.Component {

    constructor(props, context) {
        super(props, context);
        this.state = {
            openModules: []
        }
    }

    render() {
        let cmod;
        const tabs = [];
        const editors = [];
        for (let moduleName of this.state.openModules) {
            const moduleObj = this.props.moduleMap[moduleName];
            tabs.push(
                <li className="nav-item">
                    <a className="nav-link active" data-toggle="tab" href={`#${moduleName}`} role="tab">{moduleName}</a>
                </li>
            );
            editors.push(
                <div className="tab-pane active" id={moduleName} role="tabpanel">
                    <CommandModuleEditor key={moduleName} obj={moduleObj} />
                </div>
            );
        }
        return (
            <div>
                <ul className="nav nav-tabs" role="tablist">
                    {tabs}
                </ul>
                <div className="tab-content">
                    {editors}
                </div>
            </div>
        );
    }

    componentWillReceiveProps(nextProps) {
        if (nextProps.activeModule !== null &&
            !this.state.openModules.includes(nextProps.activeModule)) {
            this.setState({
                openModules: this.state.openModules.concat([nextProps.activeModule])
            });
        }
    }
    
}