
import * as React from 'react'
import { Component } from 'react';

import { Tag, Popover, Menu, MenuItem, Position, Button, ButtonGroup, Tab, Tabs, Slider, Intent, Spinner, Card, Elevation, Icon, Navbar, Alignment, Text, NonIdealState, Overlay } from "@blueprintjs/core";

import "./welcome.scss"

class Welcome extends Component {
    constructor(props) {
        super(props)
        this.state = {
            a: Math.random() * 10, b: 0.28, c: 0
        }
    }

    componentDidMount() {
        var state = this.props.pullState()
        if (state != null) {
            this.setState(state)
        }
    }

    componentWillUnmount() {
        this.props.saveState(this.state)
    }


    embedCard(whatever) {
        return (
            <Card interactive={false} elevation={Elevation.TWO}>
                {whatever}
            </Card>
        )
    }

    getChangeHandler(key) {
        return (value) => this.setState({ [key]: value });
    }

    render() {
        return (
            <div className="welcome">
                <h1>Welcome to PySOM!</h1>
                <div className="card-flex">
                    <Card interactive={true} elevation={Elevation.TWO}>
                        <h2>Start a new project</h2>
                        <Button large="true" icon="add">Start</Button>
                    </Card>
                    <Card interactive={true} elevation={Elevation.TWO}>
                        <h2>Continue with a project</h2>
                        <Button large="true" icon="folder-open">Continue</Button>
                    </Card>
                    <Card interactive={true} elevation={Elevation.TWO}>
                        <h2>Play with examples</h2>
                        <Button large="true" icon="code-block">Play</Button>
                    </Card>
                    <Card interactive={true} elevation={Elevation.TWO}>
                        <h2>Help documentation</h2>
                        <Button large="true" icon="help">Read</Button>
                    </Card>
                </div>
            </div>)

    }
}

export default Welcome;
