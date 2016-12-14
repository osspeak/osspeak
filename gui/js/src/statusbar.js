class StatusBar extends React.Component {
    render() {
        return (
            <div id="status-bar">
                <i className="fa fa-camera-retro" id="refresh-icon"></i>
                hello world i'm a bar
            </div>
        );
    }

    componentDidMount() {
        document.getElementById('refresh-icon').addEventListener('click', this.props.onSaveClick);
    }
    
}