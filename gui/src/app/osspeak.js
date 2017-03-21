import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import Application from './application';
import { createStore } from 'redux';
import { mainReducer } from './reducer';
import { initialState } from './initial-state';
import communicator from './communicator';

export const store = createStore(mainReducer, initialState);
store.subscribe(() => console.log(store.getState()));

window.onload = function() {
    ReactDOM.render(
        <Application />,
        document.getElementById('root')
    )
}