class Application extends React.Component {

    constructor(props, context) {
        super(props, context);
        this.state = {
            tree: [],
            selectedModule: null,
            moduleMap: {}
        }
    }

    render() {
        return (
            <div className="fill-parent">
                <div className="hbox">
                    <div className="vbox">
                        <CommandModuleTree data={this.state.tree} onSelect={this.updateSelectedModule.bind(this)} />
                        <EditorTabPanel moduleMap={this.state.moduleMap} selectedModule={this.state.selectedModule}/>
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
            selectedModule: this.state.selectedModule,
            moduleMap: this.state.moduleMap,
        });
    }

    updateModuleMap(data) {
        this.setState({
            tree: this.state.tree,
            selectedModule: this.state.selectedModule,
            moduleMap: data.modules,
        });
    }
    
    updateSelectedModule(moduleName) {
        this.setState({
            tree: this.state.tree,
            selectedModule: moduleName,
            moduleMap: this.state.moduleMap,
        });
    }

}