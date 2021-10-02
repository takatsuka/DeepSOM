import * as React from 'react'
import { Component } from 'react';
import Xarrow from "react-xarrows";

import { Tag, Popover, Content, Menu, MenuItem, Position, Button, ButtonGroup, Tab, Tabs, Slider, Intent, Spinner, Card, Elevation, Icon, Navbar, Alignment, Text, NonIdealState, Overlay } from "@blueprintjs/core";

import "./drag-drop.scss"

class DragDropSOM extends Component {
    constructor(props) {
        super(props);
        this.state = {x: Math.random() * 800,
                    y: Math.random() * 600,
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
        //this.onMouseUp();
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
        this.props.parent.child_update();
    }

    render() {
        var opacity = 1;
        if (this.state.dragging) {
            var opacity = 0.6;
        }

        return (<div class="som" id={"som_"+this.props.id}
                style={{top: this.state.y, left: this.state.x, opacity: opacity}}
                onMouseDown={this.onMouseDown.bind(this)}
                onMouseUp={this.onMouseUp.bind(this)}
                onMouseMove={this.onMouseMove.bind(this)}
                onMouseOut={this.onMouseOut.bind(this)}
                >
                <b style={{margin: "0 10px"}}>SOM {this.props.id}</b>
                {this.props.parent.state.add_link_active ? (
                    <Button id="addlink" icon="add" intent="success" onClick={() => this.props.parent.add_link_node(this.props.id)}/>
                ) : (
                    <Button id="deletenode" icon="trash" intent="warning" onClick={() => this.props.parent.remove_handler(this.props.id)}/>
                )}
                </div>);
    }
}

class DragDrop extends Component {
    constructor(props) {
        super(props)
        this.state = {soms: [], add_link_active: false, add_link_step: 1};

        // Bind functions
        this.add_som = this.add_som.bind(this);
        this.add_link_init = this.add_link_init.bind(this);
        this.add_link_cancel = this.add_link_cancel.bind(this);
        this.add_link_node = this.add_link_node.bind(this);
        this.render = this.render.bind(this);
        this.remove_handler = this.remove_handler.bind(this);
        this.child_update = this.child_update.bind(this);


        this.new_link_nodes = [-1, -1];
        this.links = [];
        this.i = 0;
    }

    add_som() {
        if (this.state.soms.length > 10) {
            return false;
        }

        var joined = this.state.soms.concat(this.i++);
        this.setState({ soms: joined });
    }

    add_link_init() {
        this.setState({ add_link_active: true, add_link_step: 1 });
    }

    add_link_cancel() {
        this.setState({ add_link_active: false });
    }

    add_link_node(id) {
        if (!this.state.add_link_active) return;

        if (this.state.add_link_step == 1) {
            this.new_link_nodes[0] = id;
            this.setState({ add_link_step: 2 });
        } else if (this.state.add_link_step == 2) {
            this.new_link_nodes[1] = id;
            if (!this.links.includes(this.new_link_nodes)) {
                this.links.push(this.new_link_nodes.slice(0));
            }
            this.setState({ add_link_active: false, add_link_step: -1 });
        }
    }

    remove_handler(id) {
        console.log("Delete", id);
        this.state.soms[id] = -1;
        this.setState({ soms: this.state.soms });
    }

    child_update() {
        this.setState({ render_now: true });
    }

    render() {
        const add_som_enable = this.state.soms.length < 10;
        const add_link_active = this.state.add_link_active;
        const add_link_step = this.state.add_link_step;
        const this_obj = this;

        let add_link_content = (
            <div>
                {add_link_step == 1 ? (
                    <h2>Select your first node...</h2>
                ) : (
                    <h2>Select your second node...</h2>
                )}
            </div>
        );

        return (
            <div class="som-drag-drop">
                <h1>Drag Drop SOM</h1>

                <ButtonGroup large>
                    {add_som_enable ? (
                        <Button icon="add" text="Add SOM" onClick={this.add_som} />
                    ) : (
                        <Button icon="disable" text="Add SOM" disabled="true" />
                    )}

                    <Popover content={add_link_content} popoverClassName="bp3-popover-content-sizing" onClose={this.add_link_cancel} interactionKind="CLICK_TARGET_ONLY" isOpen={add_link_active} >
                        <Button icon="new-link" text="Add Link" onClick={this.add_link_init} active={add_link_active}/>
                    </Popover>
                </ButtonGroup>

                <div class="drag-drop-box">
                    <div class="svg-box">
                    </div>

                    <div class="som-box" id="som-box">
                    {this.state.soms.map(function(d, idx){
                        if (d < 0) return null;
                        return (<DragDropSOM id={d} parent={this_obj}/>);
                    })}
                    {this.links.map(function(d, idx){
                        return (<Xarrow start={"som_"+d[0]} end={"som_"+d[1]} dashness={{animation:3}}/>);
                    })}
                    </div>
                </div>
            </div>
            );
     }
}

export default DragDrop;
