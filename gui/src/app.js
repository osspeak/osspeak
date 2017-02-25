import React, { Component } from 'react';
import ReactDOM from 'react-dom';

export const communicator = new MainProcessCommunicator('ws://localhost:8080/websocket');

window.onload = function() {
    ReactDOM.render(
        <Application />,
        document.getElementById('root')
    )
}