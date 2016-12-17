class InputField extends React.Component {
    render() {
        return (
            <input className="form-control editor-input" type="text" defaultValue={this.props.value} />
        );
    }

    componentDidMount() {
        const el = ReactDOM.findDOMNode(this);
        el.addEventListener('input', (evt) => {
            this.props.onInput(el.value, this.props.keyName);
        });
    }


}