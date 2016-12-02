let ws = new WebSocket('ws://localhost:8080/websocket');

ws.onopen = function() {
    ws.send('hello werld!');
};

ws.onmessage = function(msg) {
    console.log(msg);
};

function init() {
    ReactDOM.render(
        <Application />,
        document.getElementById('root')
    )
}