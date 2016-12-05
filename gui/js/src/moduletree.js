class CommandModuleTree extends React.Component {

    render() {
        return (
            <div id="command-module-tree" className="tree"/>
        );
    }

    componentDidMount() {
        $('#command-module-tree').jstree({
            'core' : {
                'data' : []
            }
        });
    }

    componentDidUpdate(prevProps, prevState) {
        const tree = this.tree;
        tree.settings.core.data = this.props.data;
        tree.refresh();
    }
    
    get tree() {
        return $('#command-module-tree').jstree(true);
    }

}