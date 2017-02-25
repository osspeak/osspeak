const communicator = new MainProcessCommunicator('ws://localhost:8080/websocket');

function init() {
    ReactDOM.render(
        <Application />,
        document.getElementById('root')
    )
}