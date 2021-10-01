
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
            <>
                {this.embedCard(<>
                    <h1>Welcome to PySOM {this.props.tabID}</h1>
                    {this.embedCard(
                        <div>
                            <h3>Sliders drag</h3>
                            <p>Drag the sliders then switch to another tab and back. See how their states are restored?</p>
                            <Slider
                                min={0}
                                max={10}
                                stepSize={0.1}
                                labelStepSize={10}
                                onChange={this.getChangeHandler("a")}
                                value={this.state.a}
                            />
                            <Slider
                                min={0}
                                max={0.7}
                                stepSize={0.01}
                                labelStepSize={0.14}
                                onChange={this.getChangeHandler("b")}
                                value={this.state.b}
                            />
                            <Slider
                                min={-12}
                                max={48}
                                stepSize={6}
                                labelStepSize={6}
                                onChange={this.getChangeHandler("c")}
                                showTrackFill={false}
                                value={this.state.c}
                            />
                        </div>)}
                </>)}
            </>)

    }
}

export default Welcome;
