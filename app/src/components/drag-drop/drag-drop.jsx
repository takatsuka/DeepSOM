import * as React from 'react'
import { Component } from 'react';

import { Tag, Popover, Menu, MenuItem, Position, Button, ButtonGroup, Tab, Tabs, Slider, Intent, Spinner, Card, Elevation, Icon, Navbar, Alignment, Text, NonIdealState, Overlay } from "@blueprintjs/core";

import "./drag-drop.scss"

class DragDropSOM extends Component {
    constructor(props) {
        super(props);
        this.state = {x: Math.random() * 300,
                    y: Math.random() * 300,
                    dragging: false};
    }

    onMouseDown() {
        console.log("DOWN");
        this.setState({dragging: true, prev_mouse_pos: {
            x: event.pageX,
            y: event.pageY
        }});
    }

    onMouseUp() {
        console.log("UP");
        this.setState({dragging: false});
    }

    onMouseOut() {
        this.onMouseUp();
    }

    onMouseMove(e) {
        if (!this.state.dragging) return

        var current_mouse_pos = {
            x: event.pageX,
            y: event.pageY
        };
        var dx = current_mouse_pos.x - this.state.prev_mouse_pos.x;
        var dy = current_mouse_pos.y - this.state.prev_mouse_pos.y;

        this.setState({x: this.state.x + dx, y: this.state.y + dy, prev_mouse_pos: current_mouse_pos});
    }

    render() {
        var opacity = 1;
        if (this.state.dragging) {
            var opacity = 0.6;
        }

        return (<div class="som"
                style={{top: this.state.y, left: this.state.x, opacity: opacity}}
                onMouseDown={this.onMouseDown.bind(this)}
                onMouseUp={this.onMouseUp.bind(this)}
                onMouseMove={this.onMouseMove.bind(this)}
                onMouseOut={this.onMouseOut.bind(this)}
                >SOM {this.props.id}</div>);
    }
}

class DragDrop extends Component {
    constructor(props) {
        super(props)
        this.state = {soms: []};

        // Bind functions
        this.add_som = this.add_som.bind(this);
        this.render = this.render.bind(this);
        this.i = 0;
    }

    add_som() {
        if (this.state.soms.length > 10) {
            return false;
        }

        var joined = this.state.soms.concat(this.i++);
        this.setState({ soms: joined });
    }

    render() {
        const add_som_enable = this.state.soms.length < 10;
        return (
            <div class="som-drag-drop">
                <h1>Drag Drop SOM</h1>
                {add_som_enable ? (
                    <Button icon="plus" text="Add SOM" onClick={this.add_som} />
                ) : (
                    <Button icon="cross" text="Add SOM" disabled="true" />
                )}

                <div class="drag-drop-box">
                    <div class="svg-box">
                    </div>

                    <div class="som-box" id="som-box">
                    {this.state.soms.map(function(d, idx){
                        return (<DragDropSOM id={d}/>);
                    })}
                    </div>
                </div>
            </div>
            );
     }
}

export default DragDrop;
