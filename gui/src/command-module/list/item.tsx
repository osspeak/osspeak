import React from 'react';
import ReactDOM from 'react-dom';
import classnames from 'classnames';
import './list.css'

class CommandModuleListItem extends React.Component<any, {}> {

    componentDidMount() {
    }

    render() {
        console.log(this.props.focused)
        const className = classnames({
            "cm-list-item": true,
            focused: this.props.focused,
        })
        return (
            <div className={className} onClick={() => this.props.onClick(this.props.value)}>
                {this.props.value}
            </div>
        );
    }
}

export default CommandModuleListItem;