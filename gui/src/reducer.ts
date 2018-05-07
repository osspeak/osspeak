import { combineReducers } from "redux";
import commandModule from "./command-module/duck";

const allReducers = combineReducers({
    commandModule
});

export default allReducers