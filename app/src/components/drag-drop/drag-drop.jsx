
import * as React from 'react'
import { Component } from 'react';

import { Tag, Popover, Menu, MenuItem, Position, Button, ButtonGroup, Tab, Tabs, Slider, Intent, Spinner, Card, Elevation, Icon, Navbar, Alignment, Text, NonIdealState, Overlay } from "@blueprintjs/core";

import "./drag-drop.scss"

class DragDropSOM extends Component {
    constructor(props) {
        super(props);
        this.setState({dragging: false});
        console.log("NEW");
        console.log(this.props);
    }

    onMouseDown() {
        console.log("DOWN");
        this.setState({dragging: true});
    }
    onMouseUp() {
        console.log("UP");
        this.setState({dragging: false});
    }
    onMouseMove(e) {
        if (!this.state.dragging) return
        var sombox = document.getElementById("som-box").getBoundingClientRect();

      var left = sombox.left;
      var top = sombox.top;
      var this_elem = document.getElementsByClassName("som")[0].getBoundingClientRect();
        var x = e.pageX - left - this_elem.width/2;
        var y = e.pageY - top - this_elem.height/2;
        console.log(left, top, x, y);
        this.props.DragDropObj.update_som_pos(this.props.id, x, y);
        e.stopPropagation()
        e.preventDefault()
    }

    render() {
        return (<div class="som"
                style={{top: this.props.y, left: this.props.x}}
                onMouseDown={this.onMouseDown.bind(this)}
                onMouseUp={this.onMouseUp.bind(this)}
                onMouseMove={this.onMouseMove.bind(this)}
                >SOM {this.props.id}</div>);
    }
}

class SOMContainer {
    constructor(id, x, y) {
        this.id = id;
        this.x = x;
        this.y = y;
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
            alert("NO!");
            return false;
        }
        var x = Math.random() * 300;
        var y = Math.random() * 300;
        var joined = this.state.soms.concat(new SOMContainer(this.i++, x, y));
        this.setState({ soms: joined });
    }

    update_som_pos(id, x, y) {
        this.state.soms[id].x = x;
        this.state.soms[id].y = y;
        this.setState({ soms: this.state.soms});
    }

    render() {
        const add_som_enable = this.state.soms.length < 10;
        const thisobj = this;
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
                        return (<DragDropSOM id={d.id} x={d.x} y={d.y} DragDropObj={thisobj}/>);
                    })}
                    </div>
                </div>
            </div>
            );
     }
}

export default DragDrop;
