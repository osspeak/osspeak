class CommandModuleTree extends React.Component {

    constructor(props, context) {
        super(props, context);
        this.selectedData = [];
    }
    

    render() {
        return (
            <div id="command-module-tree" className="tree"/>
        );
    }

    componentDidMount() {
        $('#command-module-tree').jstree({
            'core' : {
                'data' : []
            },
        });
        this.attachEvents();
    }

    shouldComponentUpdate(nextProps, nextState) {
        return (nextProps.data !== this.props.data)
    }
    

    componentDidUpdate(prevProps, prevState) {
        const tree = this.tree;
        tree.settings.core.data = this.props.data;
        tree.refresh();
    }
    
    get tree() {
        return $('#command-module-tree').jstree(true);
    }

    attachEvents() {
        const treeDiv = $('#command-module-tree');
        treeDiv.bind("select_node.jstree", (evt, data) => {
            this.selectedData = data;
            setTimeout(() => { if (this.selectedData === data) this.props.onSelect(this.selectedData); }, 0);
            }
        );
    }

}