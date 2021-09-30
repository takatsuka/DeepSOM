
import * as React from 'react'
import { Component } from 'react';

import { Tag, Popover, Menu, MenuItem, Position, Button, ButtonGroup, Tab, Tabs, Intent, Divider, Spinner, Card, Elevation, Icon, Navbar, Alignment, Text, NonIdealState, Overlay, Switch } from "@blueprintjs/core";
import "./scatterview.scss"

const d3 = require("d3");
import { _3d } from 'd3-3d';

class ScatterView3D extends Component {

    constructor(props) {
        super(props)

        // Bind functions
        this.initView = this.initView.bind(this);
        this.drawAxis = this.drawAxis.bind(this);
        this.updatePlot = this.updatePlot.bind(this);
        this.drawPlot = this.drawPlot.bind(this);
        this.handleShowTrainingChange = this.handleShowTrainingChange.bind(this);
        this.updateWindow = this.updateWindow.bind(this);

        this.d3view = React.createRef();

        // Define state variables
        this.state = {
            datasetName: "",
            vizData: null, hasData: false,
            showTraining: false, trainingData: null, hasTraining: false,
        }

        // Define graph variables
        this.mx = 0;
        this.my = 0;
        this.mouseX = 0;
        this.mouseY = 0;
        this.origin = [300, 300];
        this.scale = 100;
        this.startAngle = Math.PI / 4;
        this.coordinates = [];
        this.weights = [];

        // Add listener for window resize events
        window.addEventListener('resize', this.updateWindow);
    }

    componentDidMount() {
        this.initView();
        this.updateWindow();

    }

    componentWillUnmount() {
        window.removeEventListener('resize', this.updateWindow)
    }

    // Predefined function to return x coordinate for drawing purposes
    posPointX(d) {
        return d.projected.x;
    }

    // Predefined function to return y coordinate for drawing purposes
    posPointY(d) {
        return d.projected.y;
    }

    // TODO: Set colour of points accordingly to type of data
    // Draws scatter points with inputted coordinate data
    drawPoints(data, tt) {
        const svg = this.svg
        const cm = this.colorMap
        var points = svg.selectAll('circle').data(data, (d) => { d.id });
        points
            .enter()
            .append('circle')
            .attr('class', '_3d')
            .attr('opacity', 0)
            .attr('cx', this.posPointX)
            .attr('cy', this.posPointY)
            .merge(points)
            .transition().duration(tt)
            .attr('r', 3)
            .attr('stroke', (d) => d3.color(cm(d.id)).darker(3))
            .attr('fill', (d) => d3.color(cm(d.id)))
            .attr('opacity', 1)
            .attr('cx', this.posPointX)
            .attr('cy', this.posPointY);

        points.exit().remove();
    }

    // Draws axis scale and text
    drawAxis(data, axis, object) {
        const svg = this.svg

        // Determine dimension to read from and write to
        let dimension = 0;
        switch (axis) {
            case "x":
                dimension = 0;
                break;
            case "y":
                dimension = 1;
                break;
            case "z":
                dimension = 2;
                break;
            default:
                break;
        }

        // Draw scale
        let scale = svg.selectAll('path.' + axis + "Scale").data(data);
        scale
            .enter()
            .append('path')
            .attr('class', '_3d ' + axis + "Scale")
            .merge(scale)
            .attr('stroke', 'black')
            .attr('stroke-width', .5)
            .attr('d', object.draw);

        scale.exit().remove();

        // Write scale text
        let text = svg.selectAll('text.' + axis + 'Text').data(data[0]);
        text
            .enter()
            .append('text')
            .attr('class', '_3d ' + axis + 'Text')
            .attr('dx', '.3em')
            .merge(text)
            .each(function (d) {
                d.centroid = { x: d.rotated.x, y: d.rotated.y, z: d.rotated.z };
            })
            .attr('x', this.posPointX)
            .attr('y', this.posPointY)
            .text(function (d) { return d[dimension]; });

        text.exit().remove();
    }

    // Record mouse coordinate at start of drag
    dragStart(event) {
        this.mx = d3.pointer(event, this)[0];
        this.my = d3.pointer(event, this)[1];
    }

    // Record mouse coordinate at end of drag
    dragEnd(event) {
        // console.log("end drag");
        this.mouseX = d3.pointer(event, this)[0] - this.mx + this.mouseX;
        this.mouseY = d3.pointer(event, this)[1] - this.my + this.mouseY;
    }

    // Calculate where everything should be after dragging and redraw plot
    dragged(event) {
        if (!this.state.hasData) return
        this.mouseX = this.mouseX || 0;
        this.mouseY = this.mouseY || 0;
        // Calculate rotation angles
        let beta = (d3.pointer(event, this)[0] - this.mx + this.mouseX) * Math.PI / 230;
        let alpha = (d3.pointer(event, this)[1] - this.my + this.mouseY) * Math.PI / 230 * (-1);
        // Apply rotation values to d3 objects and data points
        let data = [
            this.point3d.rotateY(beta + this.startAngle).rotateX(alpha - this.startAngle)(this.coordinates[0]),
            this.weights3d.rotateY(beta + this.startAngle).rotateX(alpha - this.startAngle)(this.weights),
            this.xScale3d.rotateY(beta + this.startAngle).rotateX(alpha - this.startAngle)(this.coordinates[1]),
            this.yScale3d.rotateY(beta + this.startAngle).rotateX(alpha - this.startAngle)(this.coordinates[2]),
            this.zScale3d.rotateY(beta + this.startAngle).rotateX(alpha - this.startAngle)(this.coordinates[3])
        ];
        // Redraw plot
        this.drawPlot(data, 0);
    }


    // Function to run when file is successfully loaded and contents are read in
    // TODO: this function is kept for to remaind compatible, might be removed since load was done in python
    loadData(data) {
        var scatter = [], xLine = [], yLine = [], zLine = [];
        var counter = 0; // For assigning point IDs

        // Iterate through each line of data
        for (let i = 0; i < data.length; i++) {
            let tokens = data[i];
            let pointX = parseFloat(tokens[0]);
            let pointY = parseFloat(tokens[1]);
            let pointZ = parseFloat(tokens[2]);
            // Append float data to list
            scatter.push({ x: pointX, y: pointY, z: pointZ, id: 'point_' + counter++ });
        }

        // Define values for xyz scales
        for (let i = -1; i <= 1; i = i + 0.5) {
            xLine.push([-i, 1, -1]);
            yLine.push([-1, i, -1]);
            zLine.push([-1, 1, -i]);
        }

        // Input data for d3 drawing
        let input = [
            scatter,
            [xLine],
            [yLine],
            [zLine]
        ];

        return input;
    }

    // To accept a data file from the upload point on ScatterView
    // TODO: this function is kept for to remaind compatible, might be removed since load was done in python
    importDataFile() {
        window.pywebview.api.open_csv_file().then((d) => {
            this.setState({ vizData: d[1], hasData: true, datasetName: d[0], showTraining: false })
            this.coordinates = this.loadData(this.state.vizData);
            this.updatePlot();
        })
    }

    // To accept a weights file from the upload point on ScatterView
    // TODO: this function is kept for to remaind compatible, might be removed since load was done in python
    importWeightsFile() {
        window.pywebview.api.open_csv_file().then((d) => {
            this.setState({ trainingData: d[1], hasTraining: true, showTraining: true });
            this.weights = this.loadData(this.state.trainingData)[0];
            this.updatePlot();
        });
    }

    // Draws the scatter points and 3 axes
    drawPlot(result, tt) {
        this.drawPoints(result[0], tt);
        if (this.state.showTraining) {
            this.drawPoints(result[1], tt);
        }
        this.drawAxis(result[2], 'x', this.xScale3d);
        this.drawAxis(result[3], 'y', this.yScale3d);
        this.drawAxis(result[4], 'z', this.zScale3d);
    }

    // Function to update the current plot and redraw, created for slider feature when moving between plots
    updatePlot() {
        let result = [
            this.point3d(this.coordinates[0]),
            this.weights3d(this.weights),
            this.xScale3d(this.coordinates[1]),
            this.yScale3d(this.coordinates[2]),
            this.zScale3d(this.coordinates[3]),
        ];

        this.drawPlot(result, 0);
    }

    initView() {
        /* -------- d3 object initialisations -------- */
        const svg = d3.select(this.d3view.current)
            .call(d3.drag()
                .on('start', event => {
                    this.dragStart(event);
                })
                .on('end', event => {
                    this.dragEnd(event);
                })
                .on('drag', event => {
                    this.dragged(event);
                })
            ).append('g');

        this.svg = svg
        this.colorMap = d3.scaleOrdinal(d3.schemeCategory10);

        // Data points
        this.point3d = _3d()
            .x(function (d) { return d.x; })
            .y(function (d) { return -d.y; })
            .z(function (d) { return d.z; })
            .origin(this.origin)
            .rotateY(this.startAngle)
            .rotateX(-this.startAngle)
            .scale(this.scale);

        // Weight points
        this.weights3d = _3d()
            .x(function (d) { return d.x; })
            .y(function (d) { return -d.y; })
            .z(function (d) { return d.z; })
            .origin(this.origin)
            .rotateY(this.startAngle)
            .rotateX(-this.startAngle)
            .scale(this.scale);

        // X axis
        this.xScale3d = _3d()
            .shape('LINE_STRIP')
            .origin(this.origin)
            .rotateY(this.startAngle)
            .rotateX(-this.startAngle)
            .scale(this.scale);

        // Y axis
        this.yScale3d = _3d()
            .shape('LINE_STRIP')
            .origin(this.origin)
            .rotateY(this.startAngle)
            .rotateX(-this.startAngle)
            .scale(this.scale);

        // Z axis
        this.zScale3d = _3d()
            .shape('LINE_STRIP')
            .origin(this.origin)
            .rotateY(this.startAngle)
            .rotateX(-this.startAngle)
            .scale(this.scale);
    }

    // Updates the origin and scale of d3 objects according to adjusted window size
    updateObjects() {
        // Data points
        this.point3d.origin(this.origin).scale(this.scale);
        // Weight points
        this.weights3d.origin(this.origin).scale(this.scale);
        // X axis
        this.xScale3d.origin(this.origin).scale(this.scale);
        // Y axis
        this.yScale3d.origin(this.origin).scale(this.scale);
        // Z axis
        this.zScale3d.origin(this.origin).scale(this.scale);
    }

    // Reads in adjusted window size to calculate origin and scale of d3 objects
    updateWindow() {
        let innerWidth = window.innerWidth - 180;
        let innerHeight = window.innerHeight - 120;
        this.origin = [innerWidth / 2, innerHeight / 2];
        this.scale = innerWidth / 620 > innerHeight / 480 ? innerHeight / 480 * 100 : innerWidth / 620 * 100;
        console.log(this.scale);
        this.updateObjects();
        if (this.state.hasData) this.updatePlot();
    }

    // Function to update state on whether to show SOM training data or not based on slider
    handleShowTrainingChange() {
        this.setState((state) => {
            return { showTraining: !state.showTraining }
        }, () => { this.updatePlot(); });
    }

    embedCard(whatever) {
        return (
            <Card interactive={false} elevation={Elevation.TWO}>
                {whatever}
            </Card>
        )
    }

    render() {
        return (
            <>
                <div className="submenu">
                    <ButtonGroup style={{ minWidth: 200 }} minimal={true} className="sm-buttong">
                        {this.state.hasData ?
                            <>
                                <Switch disabled={!this.state.hasTraining} className="switch"
                                    checked={this.state.showTraining}
                                    label="Show training"
                                    onChange={this.handleShowTrainingChange} />
                                    
                                <Button disabled={true} >{this.state.datasetName}</Button>
                                <Divider />
                            </>
                            :
                            <></>
                        }

                        <Button icon="document" onClick={() => this.importDataFile()}>Load Data</Button>
                        <Button icon="document" disabled={!this.state.hasData} onClick={() => this.importWeightsFile()}>Load Weights</Button>
                    </ButtonGroup>


                </div>
                <svg className="svg-render" ref={this.d3view} />

            </>)

    }
}

export default ScatterView3D;
