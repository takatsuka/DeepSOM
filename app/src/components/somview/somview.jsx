
import * as React from 'react'
import { Component } from 'react';

import { Tag, Popover, Menu, MenuItem, Position, Button, ButtonGroup, Tab, Tabs, Slider, Intent, Spinner, Card, Elevation, Icon, Navbar, Alignment, Text, NonIdealState, Overlay } from "@blueprintjs/core";


import Split from 'react-split'
import SplitPane, { Pane } from 'react-split-pane';
import "../common/splitview.scss"
import Canvas from "../common/canvas"
import "./somview.scss"



const d3 = require("d3");

class SOMView extends Component {
    constructor(props) {
        super(props)
        this.d3view = React.createRef();
        this.resultView = React.createRef();
        this.state = {
            somDim: 10, dotRadius: 10, img: null, services: null,
            resultViewSize: 100,
        }


        this.selector = []
    }

    componentDidMount() {
        var init = this.props.pullInit()
        if (init != null) {
            this.loadData()
        }

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

    drag(simulation) {
        const somview = this
        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(1.3).restart();
            event.subject.fx = event.subject.x;
            event.subject.fy = event.subject.y;

            d3.select(this).transition()
                .attr("fill", "#FFB366")
                .attr("r", somview.state.dotRadius * 1.5)


        }

        function dragged(event) {
            event.subject.fx = event.x;
            event.subject.fy = event.y;
        }

        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            event.subject.fx = null;
            event.subject.fy = null;

            d3.select(this).transition()
                .attr("fill", "#10161A")
                .attr("r", somview.state.dotRadius);

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

    rectLinks(dim) {
        var links = []
        for (let y = 0; y < dim; y++) {
            for (let x = 0; x < dim - 1; x++) {
                let row = y * dim
                links.push({ "source": row + x, "target": row + x+1, "value": 26 })
            }
        }

        for (let y = 0; y < dim - 1; y++) {
            for (let x = 0; x < dim; x++) {
                let row = y * dim
                links.push({ "source": row + x, "target": row + x + dim, "value": 30 })
            }
        }

        return links
    }

    resizeViews() {
        this.selector = []
        this.initSOMView()
    }

    zoomed(transform) {
        d3.select(this.d3view.current).selectAll('g').attr("transform", transform);
    }

    initSOMView() {
        var margin = 30
        var w = this.d3view.current.clientWidth
        var h = this.d3view.current.clientHeight
        var gridSize = Math.min(w, h) - this.state.dotRadius * 2 - margin * 2
        var spacing = gridSize / (this.state.somDim - 1)
        var horMarg = this.state.dotRadius
        var verMarg = h * 0.5 - (gridSize * 0.5)

        var nodes = [...Array(this.state.somDim * this.state.somDim).keys()].map((e) => ({
            id: e
        }))
        var links = this.rectLinks(this.state.somDim)

        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.id).strength(1.0).distance((d) => d.value).iterations(15))
            .force("charge", d3.forceManyBody().strength(-30))
            .force("center", d3.forceCenter(w / 2, h / 2))

        const zoom = d3.zoom()
            .extent([[0, 0], [w, h]])
            .scaleExtent([0.5, 100])
            .on("zoom", ({ transform }) => {
                this.zoomed(transform)
            })




        const svg = d3.select(this.d3view.current)
        svg.call(zoom);
        svg.selectAll('*').remove()
        const nodeG = svg.append("g")
            .attr("stroke", "#fff")
            .attr("stroke-width", 0.2)
        const n = nodeG.selectAll("circle")
            .data(nodes)
            .join("circle")
            .attr("r", this.state.dotRadius)
            .attr("fill", "#10161A")
            .call(this.drag(simulation))

        this.n_c = n
        this.nodeg = nodeG

        const l = svg.append("g")
            .attr("stroke", "#555")
            .attr("stroke-width", 0.5)
            .selectAll("line")
            .data(links)
            .join("line")
            .attr("stroke", "#182026")
        this.linkline = l


        // const t = this.nodeg.selectAll("text")
        //     .data(nodes)
        //     .join("text")
        //     .style("fill", "white")
        //     .style("font-size", 4)
        //     .text(d => d.id)
        //     .attr("stroke-width", 0)
        //     .attr("text-anchor", "middle")
        //     .attr("dy", 6)

        simulation.on("tick", () => {
            l
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            n
                .attr("cx", d => d.x)
                .attr("cy", d => d.y);


            // t
            //     .attr("x", d => d.x)
            //     .attr("y", d => d.y);

        });
    }

    render() {
        return (
            <>
                <div className="submenu">
                    <ButtonGroup style={{ minWidth: 200 }} minimal={true} className="sm-buttong">
                        <Button icon="document" onClick={() => this.loadData()}>Select SOM</Button>
                        <Button icon="document" onClick={() => this.resizeViews()}>Reinit View</Button>
                    </ButtonGroup>
                </div>
                <div className="somview-graph-area" >
                    <div className="som">
                        <svg className="imviewsvg-render" ref={this.d3view} />
                    </div>

                </div>

            </>)

    }
}

export default SOMView;
