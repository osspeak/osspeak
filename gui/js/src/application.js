class Application extends React.Component {

    constructor(props, context) {
        super(props, context);
        this.state = {
            tree: [],
            selectedModules: null,
            moduleMap: {}
        }
    }

    render() {
        return (
            <div className="fill-parent">
                <div className="hbox">
                    <div className="vbox">
                        <CommandModuleTree data={this.state.tree} onSelect={this.updateSelectedModules.bind(this)} />
                        <CommandModuleEditor />
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
            selectedModules: this.state.selectedModules,
            moduleMap: this.state.moduleMap,
        });
    }

    updateModuleMap(data) {
        this.setState({
            tree: this.state.tree,
            selectedModules: this.state.selectedModules,
            moduleMap: data.modules,
        });
    }
    
    updateSelectedModules(data) {
        console.log(data.selected);
        //if (data.selected.length === 1) return;
        this.setState({
            tree: this.state.tree,
            selectedModules: data.selected,
            //selectedModules: [],
            moduleMap: this.state.moduleMap,
        });
    }

}