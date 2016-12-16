class CommandModuleTree extends React.Component {

    constructor(props, context) {
        super(props, context);
        this.selected = null
    }
    
    render() {
        return (
            <div id="command-module-tree" className="tree" />
        );
    }

    componentDidMount() {
        $('#command-module-tree').jstree({
            'core' : {
                'data' : [],
                'multiple': false,
            },
        });
        this.attachEvents();
    }

    componentWillReceiveProps(nextProps) {
        if (this.selected !== nextProps.selected) {
            $('#command-module-tree').jstree("deselect_all");
            $('#command-module-tree').jstree('select_node', nextProps.selected);
        }
    }

    shouldComponentUpdate(nextProps, nextState) {
        return nextProps.data !== this.props.data;
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
            // can't select parent nodes
            if (data.node.children.length > 0) {
                data.instance.deselect_node(data.node);                    
                data.instance.select_node(this.selected);                    
            }
            else {
                this.selected = data.selected[0];
                this.props.onSelect(data.selected[0]);
            }
        });
    }
}