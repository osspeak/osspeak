import React from 'react';
import ReactDOM from 'react-dom';
import { wsFetch } from '../websocket';
import { Button } from 'material-ui'
import { Treebeard } from 'react-treebeard';
import { List, ListItem, ListItemIcon, ListItemText, Divider } from 'material-ui';

class CommandModuleList extends React.Component<any, {}> {

    componentDidMount() {
    }

    render() {
        return (
            <div>
                <List component="nav">
                    <ListItem button>
                        <ListItemText primary="Inbox" />
                    </ListItem>
                    <ListItem button>
                        <ListItemText primary="Drafts" />
                    </ListItem>
                </List>
                <Divider />
                <List component="nav">
                    <ListItem button>
                        <ListItemText primary="Trash" />
                    </ListItem>
                    <ListItem button component="a" href="#simple-list">
                        <ListItemText primary="Spam" />
                    </ListItem>
                </List>
            </div>
        );
    }
}

export default CommandModuleList;