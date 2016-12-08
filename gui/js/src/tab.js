class Tab extends React.Component {
    render() {
        return (
            <li key={this.props.title} className="nav-item">
                <a className={`nav-link ${this.props.active}`} data-toggle="tab" href={`#${this.props.title}`} role="tab">{this.props.title}</a>
            </li>
        );
    }

    componentDidMount() {
        const el = ReactDOM.findDOMNode(this).querySelector('.nav-link');
        el.addEventListener('click', (evt) => {
            this.props.onClick(this.props.title);
        });
    }
}