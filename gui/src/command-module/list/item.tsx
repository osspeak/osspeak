import React from 'react';
import ReactDOM from 'react-dom';

class CommandModuleListItem extends React.Component<any, {}> {

    componentDidMount() {
    }

    render() {
        return (
            <div className="cm-list-item" onClick={() => this.props.onClick(this.props.value)}>
                {this.props.value}
            </div>
        );
    }
}

export default CommandModuleListItem;