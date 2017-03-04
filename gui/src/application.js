export default class Application extends React.Component {

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
            <div className="vbox fill-parent">
                <div className="hbox">
                    <CommandModuleTree
                        selected={this.state.activeModule}
                        moduleMap={this.state.moduleMap}
                        data={this.state.tree}
                        onSelect={this.updateActiveModule.bind(this)}
                    />
                    <EditorTabPanel
                        onTabClick={this.updateActiveModule.bind(this)}
                        onSaveClick={this.saveModules.bind(this)}
                        moduleMap={this.state.moduleMap}
                        activeModule={this.state.activeModule}
                        onFieldInput={this.mutateModuleMap.bind(this)}
                    />
                </div>
            </div>
        );
    }

    componentDidMount() {
        communicator.subscribe('module map', this.updateModuleMap.bind(this));
        document.onkeydown = this.keyPress.bind(this);
    }

    updateModuleMap(data) {
        console.log(data.modules);
        this.setState({moduleMap: data.modules});
    }

    mutateModuleMap(action, data={}) {
        let newModules;
        switch (action) {
            case 'setItem':
                newModules = modules.setItem(this.state.moduleMap, data);
                this.setState({moduleMap: newModules});
        }
    }
    
    updateActiveModule(moduleName) {
        this.setState({activeModule: moduleName});
    }

    keyPress(evt) {
        if (evt.key === 's' && evt.ctrlKey) this.saveModules();
    }

    saveModules() {
        communicator.sendMessage('save modules', {modules: this.state.moduleMap});
    }

}