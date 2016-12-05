class Application extends React.Component {

    constructor(props, context) {
        super(props, context);
        this.state = {
            tree: []
        }
    }

    render() {
        return (
            <div className="fill-parent">
                <CommandModuleTree data={this.state.tree} />
            </div>
        );
    }

    componentDidMount() {
        communicator.subscribe('display module tree', this.updateTree.bind(this));
    }

    updateTree(data) {
        this.setState({
            tree: data.tree   
        });
    }
    

}