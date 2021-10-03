
import * as React from 'react'
import { Component } from 'react';

import { Tag, Popover, Menu, MenuItem, Position, Button, ButtonGroup, Tab, Tabs, Slider, Intent, Spinner, Card, Elevation, Icon, Navbar, Alignment, Text, NonIdealState, Overlay } from "@blueprintjs/core";

import SplitPane, { Pane } from 'react-split-pane';
import "../common/splitview.scss"
import Canvas from "../common/canvas"
import "./imageview.scss"

const d3 = require("d3");

class ImageView extends Component {
    constructor(props) {
        super(props)
        this.d3view = React.createRef();
        this.state = {
            somDim: 10, dotRadius: 3, img: null
        }


        this.selector = []
    }

    componentDidMount() {
        var state = this.props.pullState()
        if (state != null) {
            this.setState(state)
        }

        this.initSOMView()

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

    somSelectorDrag() {
        const self = this

        function dragstarted(event, d) {
        }

        function dragged(event) {
            d3.select(this)
                .attr("cx", event.x)
                .attr("cy", event.y)

            self.selector = [{ x: event.x, y: event.y }]
        }

        function dragended(event, d) {
            self.initSOMView()
            // console.log(self.services)


        }

        return d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended);
    }

    loadData() {
        var self = this
        console.log(window.pywebview.api)
        window.pywebview.api.launch_service("SOMVisualizationService").then((x) => (
            self.services = x
        ))
        
    }

    resizeViews() {
        this.selector = []
        this.initSOMView()
    }

    initSOMView() {
        var margin = 30
        var w = this.d3view.current.clientWidth
        var h = this.d3view.current.clientHeight
        var gridSize = Math.min(w, h) - this.state.dotRadius * 2 - margin * 2
        var spacing = gridSize / (this.state.somDim - 1)
        var horMarg = this.state.dotRadius
        var verMarg = h * 0.5 - (gridSize)

        var grid = [...Array(this.state.somDim).keys()].map(
            (y) => ([...Array(this.state.somDim).keys()].map(
                (x) => ({ x: x * spacing + horMarg + margin, y: y * spacing + verMarg + margin })
            ))
        ).flat()

        if (this.selector.length < 1) this.selector.push(grid[0])
        else {
            var coord = this.selector[0]
            var ori = { x: (coord.x - (horMarg + margin)) / gridSize, y: (coord.y - (verMarg + margin)) / gridSize }
            var somC = { x: ori.x * this.state.somDim, y: ori.y * this.state.somDim }
            console.log(somC)
            var self = this
            window.pywebview.api.call_service(this.services, "position", [somC.x,somC.y]).then((x) => (
                // console.log(x)
                self.setState({
                    img: x
                })
            ))
        }

        const svg = d3.select(this.d3view.current)
        svg.selectAll('*').remove()
        svg.append("g")
            .attr("stroke", "#fff")
            .attr("stroke-width", 1.5)
            .selectAll("circle")
            .data(grid)
            .join("circle")
            .attr("cx", (d) => (d.x))
            .attr("cy", (d) => (d.y))
            .attr("r", this.state.dotRadius)
            .attr("fill", "#202B33")

        svg.append("g")
            .attr("stroke", "#fff")
            .attr("stroke-width", 1.5)
            .selectAll("circle")
            .data(this.selector)
            .join("circle")
            .attr("cx", (d) => (d.x))
            .attr("cy", (d) => (d.y))
            .attr("r", 8)
            .attr("fill", "#5C7080")
            .call(this.somSelectorDrag())


    }

    render() {
        return (
            <>


                <div>
                    <SplitPane split="vertical" minSize={300}>

                        <div className="som">
                            <div className="submenu">
                                <ButtonGroup style={{ minWidth: 200 }} minimal={true} className="sm-buttong">
                                    <Button icon="document" onClick={() => this.loadData()}>Load Data</Button>
                                    <Button icon="document" onClick={() => this.resizeViews()}>Resize</Button>
                                </ButtonGroup>


                            </div>
                            <svg className="svg-render" ref={this.d3view} />
                        </div>

                        <div className="result">
                            {this.state.img == null ? <div/> : <Canvas w="4" h="4" className="visview" canvasClass="visview" data={this.state.img}/>}
                        </div>


                    </SplitPane>
                </div>



            </>)

    }
}

export default ImageView;
