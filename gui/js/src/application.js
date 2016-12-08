class Application extends React.Component {

    constructor(props, context) {
        super(props, context);
        this.state = {
            tree: [],
            activeModule: null,
            moduleMap: {}
        }
    }

    render() {
        return (
            <div className="fill-parent">
                <div className="hbox">
                    <div className="vbox">
                        <CommandModuleTree selected={this.state.activeModule} data={this.state.tree} onSelect={this.updateActiveModule.bind(this)} />
                        <EditorTabPanel onTabClick={this.updateActiveModule.bind(this)} moduleMap={this.state.moduleMap} activeModule={this.state.activeModule}/>
                    </div>
                </div>
            </div>
        );
    }

    componentDidMount() {
        communicator.subscribe('display module tree', this.updateTree.bind(this));
        communicator.subscribe('module map', this.updateModuleMap.bind(this));
    }

    updateTree(data) {
        this.setState({tree: data.tree});
    }

    updateModuleMap(data) {
        this.setState({moduleMap: data.modules});
    }
    
    updateActiveModule(moduleName) {
        this.setState({activeModule: moduleName});
    }

}