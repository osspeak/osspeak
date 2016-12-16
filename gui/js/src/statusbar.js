class StatusBar extends React.Component {
    render() {
        return (
            <div id="status-bar">
                <i className="fa fa-camera-retro" id="refresh-icon"></i>
            </div>
        );
    }

    componentDidMount() {
        document.getElementById('refresh-icon').addEventListener('click', this.props.onSaveClick);
    }
    
}