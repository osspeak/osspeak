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
        if (!this.hasSameProps(this.props.moduleMap, nextProps.moduleMap)) {
            const tree = this.tree;
            tree.settings.core.data = this.data(nextProps.moduleMap);
            tree.refresh();
        }
        if (this.selected !== nextProps.selected) {
            $('#command-module-tree').jstree("deselect_all");
            $('#command-module-tree').jstree('select_node', nextProps.selected);
        }
    }

    shouldComponentUpdate(nextProps, nextState) {
        return false;
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

    data(moduleMap) {
        const nodeMap = {'': {'children': []}};
        for (let path of Object.keys(moduleMap)) {
            let splitPath = path.split('\\');
            this.addTreeNode(splitPath, nodeMap);
        }
        return nodeMap[''].children;
    }

    addTreeNode(path, nodeMap) {
        let parent = nodeMap[''].children;
        let partialPath = '';
        for (var i = 0; i < path.length - 1; i++) {
            let directory = path[i];
            partialPath += '\\' + directory;
            if (nodeMap[partialPath] === undefined) {
                let node = {'text': directory, 'children': [], 'id': partialPath};
                nodeMap[partialPath] = node;
                parent.push(node);
            }
            parent = nodeMap[partialPath]['children'];
        }
        parent.push({'text': path[path.length - 1], 'id': path.join('\\')})
    }

    hasSameProps(obj1, obj2) {
        const overlap1 = Object.keys(obj1).every(function(prop) {
            return obj2.hasOwnProperty(prop);
        });
        return overlap1 && Object.keys(obj2).every(function(prop) {
            return obj1.hasOwnProperty(prop);
        });
    }
}