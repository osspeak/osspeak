class FieldGroup extends React.Component {

    render() {
        return (
            <div className="hbox">
                <InputField index={0} value={this.props.textObj[0]} onInput={this.props.onFieldInput} />
                <i className="fa fa-long-arrow-right"></i>
                <InputField index={1} value={this.props.textObj[1]} onInput={this.props.onFieldInput} />
            </div>
        );
    }

}