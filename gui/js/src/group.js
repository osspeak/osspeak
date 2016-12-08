class ModuleGroup extends React.Component {
    render() {
        const fields = [];
        for (let textObj of this.props.textObjs) {
            fields.push(<FieldGroup type={this.props.title.toLowerCase()} textObj={textObj} />);
        }
        return (
            <div>
                <h1>{this.props.title}</h1>
                {fields}
            </div>
        );
    }
}