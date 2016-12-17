class InputField extends React.Component {
    render() {
        return (
            <input className="form-control editor-input" type="text" defaultValue={this.props.value} />
        );
    }

    componentDidMount() {
        const el = ReactDOM.findDOMNode(this);
        el.addEventListener('input', (evt) => {
            console.log(el.value);
            this.props.onInput(el.value);
        });
    }


}