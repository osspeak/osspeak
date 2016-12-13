class EditorTabPanel extends React.Component {

    constructor(props, context) {
        super(props, context);
        this.state = {
            openModules: []
        }
    }

    render() {
        const tabs = this.tabItems;
        const editors = this.editorItems;
        return (
            <div id="editor-panel">
                <ul className="nav nav-tabs" role="tablist">
                    {tabs}
                </ul>
                <div className="tab-content">
                    {editors}
                </div>
            </div>
        );
    }

    get tabItems() {
        const tabs = [];
        for (let moduleName of this.state.openModules) {
            let active = moduleName === this.props.activeModule ? 'active' : '';
            tabs.push(<Tab key={moduleName} onClick={this.props.onTabClick} title={moduleName} active={active} />);
        }
        return tabs;
    }

    get editorItems() {
        const editors = [];
        for (let moduleName of this.state.openModules) {
            let active = moduleName === this.props.activeModule ? 'active' : '';
            let moduleObj = this.props.moduleMap[moduleName];
            editors.push(
                <div key={moduleName} className={`tab-pane ${active}`} id={moduleName} role="tabpanel">
                    <CommandModuleEditor module={moduleObj} />
                </div>
            );
        }
        return editors;
    }

    componentWillReceiveProps(nextProps) {
        const el = ReactDOM.findDOMNode(this);
        const linkItems = el.getElementsByClassName('nav-link');
        for (let item of linkItems) {
            item.classList.remove('active');
        }
        if (nextProps.activeModule !== null &&
            !this.state.openModules.includes(nextProps.activeModule)) {
            this.setState({
                openModules: this.state.openModules.concat([nextProps.activeModule])
            });
        }
    }
    
}