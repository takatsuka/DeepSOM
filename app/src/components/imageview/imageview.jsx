
import * as React from 'react'
import { Component } from 'react';

import { Tag, Popover, Menu, MenuItem, Position, Button, ButtonGroup, Tab, Tabs, Slider, Intent, Spinner, Card, Elevation, Icon, Navbar, Alignment, Text, NonIdealState, Overlay } from "@blueprintjs/core";


import Split from 'react-split'
import SplitPane, { Pane } from 'react-split-pane';
import "../common/splitview.scss"
import Canvas from "../common/canvas"
import "./imageview.scss"



const d3 = require("d3");

class ImageView extends Component {
    constructor(props) {
        super(props)
        this.d3view = React.createRef();
        this.resultView = React.createRef();
        this.state = {
            somDim: 10, dotRadius: 4, img: null, services: null,
            resultViewSize: 100
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
            self.initSOMView(true)
        }

        function dragended(event, d) {
            self.initSOMView(false)
        }

        return d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended);
    }

    loadData() {
        var self = this
        window.pywebview.api.launch_service("SOMVisualizationService").then((x) => (
            self.setState({ services: x }, () => (
                window.pywebview.api.call_service(self.state.services, "get_dim", []).then((y) => (
                    self.setState({ somDim: y }, () => self.initSOMView(false))
                ))
            ))
        ))

    }

    resizeViews() {
        this.selector = []
        this.initSOMView()
    }

    initSOMView(resultOnly) {
        var margin = 30
        var w = this.d3view.current.clientWidth
        var h = this.d3view.current.clientHeight
        var gridSize = Math.min(w, h) - this.state.dotRadius * 2 - margin * 2
        var spacing = gridSize / (this.state.somDim - 1)
        var horMarg = this.state.dotRadius
        var verMarg = h * 0.5 - (gridSize * 0.5)

        if (this.selector.length < 1) this.selector.push({ x: horMarg + margin, y: verMarg + margin })
        else {
            var coord = this.selector[0]
            var ori = { x: (coord.x - (horMarg + margin)) / gridSize, y: (coord.y - (verMarg + margin)) / gridSize }
            var somC = { x: ori.x * (this.state.somDim-1), y: ori.y * (this.state.somDim-1) }
            console.log(somC)
            var self = this
            if (this.state.services != null) {
                window.pywebview.api.call_service(this.state.services, "position", [somC.x, somC.y]).then((x) => (
                    
                    self.setState({
                        img: x
                    })
                ))
            }
        }

        if (resultOnly) return

        var dots = [...Array(this.state.somDim).keys()].map(
            (y) => ([...Array(this.state.somDim).keys()].map(
                (x) => ({ x: x * spacing + horMarg + margin, y: y * spacing + verMarg + margin })
            ))
        )

        var grid = dots.flat()

        var lines = [...Array(this.state.somDim).keys()].map((x) => (
            {
                x1: horMarg + margin, y1: x * spacing + verMarg + margin,
                x2: horMarg + margin + (this.state.somDim - 1) * spacing, y2: x * spacing + verMarg + margin
            }
        ))

        var vlines = [...Array(this.state.somDim).keys()].map((x) => (
            {
                x1: x * spacing + horMarg + margin, y1: verMarg + margin,
                x2: x * spacing + horMarg + margin, y2: (this.state.somDim - 1) * spacing + verMarg + margin
            }
        ))
        lines = lines.concat(vlines)

        const svg = d3.select(this.d3view.current)
        svg.selectAll('*').remove()
        svg.append("g")
            .attr("stroke", "#fff")
            .attr("stroke-width", 0.2)
            .selectAll("circle")
            .data(grid)
            .join("circle")
            .attr("cx", (d) => (d.x))
            .attr("cy", (d) => (d.y))
            .attr("r", this.state.dotRadius)
            .attr("fill", "#10161A")

        svg.append("g")
            .attr("stroke", "#555")
            .attr("stroke-width", 0.5)
            .selectAll("line")
            .data(lines)
            .join("line")
            .attr("x1", (d) => (d.x1))
            .attr("x2", (d) => (d.x2))
            .attr("y1", (d) => (d.y1))
            .attr("y2", (d) => (d.y2))
            .attr("stroke", "#182026")

        svg.append("g")
            .attr("stroke", "#fff")
            .attr("stroke-width", 0.5)
            .selectAll("circle")
            .data(this.selector)
            .join("circle")
            .attr("cx", (d) => (d.x))
            .attr("cy", (d) => (d.y))
            .attr("r", 12)
            .attr("fill", "#C22762")
            .call(this.somSelectorDrag())



    }

    render() {
        return (
            <>
                <div className="submenu">
                    <ButtonGroup style={{ minWidth: 200 }} minimal={true} className="sm-buttong">
                        <Button icon="document" onClick={() => this.loadData()}>Load Data</Button>
                        <Button icon="document" onClick={() => this.resizeViews()}>Recenter</Button>
                    </ButtonGroup>
                </div>
                <Split className="imviewgraph-area" gutterSize={6} onDrag={() => this.initSOMView()}>
                    <div className="som">
                        <svg className="imviewsvg-render" ref={this.d3view} />
                    </div>
                    <div className="result" ref={this.resultView}>
                        {this.state.img == null ? <div /> : <Canvas w={28} h={28} className="visview"
                            canvasClass="visview" data={this.state.img} />}
                    </div>
                </Split>

            </>)

    }
}

export default ImageView;
