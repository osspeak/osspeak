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
                        <CommandModuleTree data={this.state.tree} onSelect={this.updateActiveModule.bind(this)} />
                        <EditorTabPanel moduleMap={this.state.moduleMap} activeModule={this.state.activeModule}/>
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
        this.setState({
            tree: data.tree,
            activeModule: this.state.activeModule,
            moduleMap: this.state.moduleMap,
        });
    }

    updateModuleMap(data) {
        this.setState({
            tree: this.state.tree,
            activeModule: this.state.activeModule,
            moduleMap: data.modules,
        });
    }
    
    updateActiveModule(moduleName) {
        this.setState({
            tree: this.state.tree,
            activeModule: moduleName,
            moduleMap: this.state.moduleMap,
        });
    }

}