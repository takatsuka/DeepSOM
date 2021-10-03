
import * as React from 'react'
import { Component } from 'react';

import { Tag, Popover, Menu, MenuItem, Slider, Button, ButtonGroup, Tab, Tabs, Intent, Divider, Spinner, Card, Elevation, Icon, Navbar, Alignment, Text, NonIdealState, Overlay, Switch } from "@blueprintjs/core";
import "./scatterview.scss"
const d3 = require("d3");
import { _3d } from 'd3-3d';

class ScatterView3D extends Component {

    constructor(props) {
        super(props);

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
            showTraining: false,
            vizData: null, hasDataset: false, dataset: [],
            trainingData: null, hasTraining: false, weights: [], weightsId: 0, edges: [], somHeight: 20, somWidth: 20,
            point3d: null, weights3d: null, xScale3d: null, yScale3d: null, zScale3d: null,
            mouseX: 0, mouseY: 0,
        }

        // Define graph variables
        this.mx = 0;
        this.my = 0;
        this.mouseX = 0;
        this.mouseY = 0;
        this.origin = [300, 300];
        this.scale = 100;
        this.startAngle = Math.PI / 4;

        // Add listener for window resize events
        window.addEventListener('resize', this.updateWindow);
    }

    componentDidMount() {
        var state = this.props.pullState();
        if (state != null && state.hasDataset) {
            // If there was a previous dataset already loaded
            this.setState(state, () => {
                this.updateSvg();
                this.updatePlot();
                this.updateWindow();
            });

        } else {
            // If there wasn't a previous dataset loaded
            this.initView();
            this.updateWindow();
        }
    }

    componentWillUnmount() {
        window.removeEventListener('resize', this.updateWindow);
        this.props.saveState(this.state);
    }

    // Predefined function to return x coordinate for drawing purposes
    posPointX(d) {
        return d.projected.x;
    }

    // Predefined function to return y coordinate for drawing purposes
    posPointY(d) {
        return d.projected.y;
    }

    // Draws surface of weight nodes with inputted json data
    drawEdges(data) {
        console.log("drawing edges");
        const svg = this.svg
        let lines = svg.selectAll('line').data(data);

        lines
            .enter()
            .append('line')
            .attr('class', '_3d')
            .merge(lines)
            .attr('fill', d3.color('steelblue'))
            .attr('stroke', d3.color('steelblue'))
            .attr('stroke-width', 0.6)
            .attr('x1', function (d) { return d[0].projected.x; })
            .attr('y1', function (d) { return d[0].projected.y; })
            .attr('x2', function (d) { return d[1].projected.x; })
            .attr('y2', function (d) { return d[1].projected.y; });

        lines.exit().remove();
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
        this.mouseX = d3.pointer(event, this)[0] - this.mx + this.mouseX;
        this.mouseY = d3.pointer(event, this)[1] - this.my + this.mouseY;
        this.setState({ mouseX: this.mouseX, mouseY: this.mouseY });
    }

    // Calculate where everything should be after dragging and redraw plot
    dragged(event) {
        if (!this.state.hasDataset) return
        this.mouseX = this.state.mouseX || 0;
        this.mouseY = this.state.mouseY || 0;
        // Calculate rotation angles
        let beta = (d3.pointer(event, this)[0] - this.mx + this.mouseX) * Math.PI / 230;
        let alpha = (d3.pointer(event, this)[1] - this.my + this.mouseY) * Math.PI / 230 * (-1);
        // Apply rotation values to d3 objects and data points
        let data = [
            this.state.point3d.rotateY(beta + this.startAngle).rotateX(alpha - this.startAngle)(this.state.showTraining ? this.state.weights : this.state.dataset[0]),
            this.state.weights3d.rotateY(beta + this.startAngle).rotateX(alpha - this.startAngle)(this.state.edges),
            this.state.xScale3d.rotateY(beta + this.startAngle).rotateX(alpha - this.startAngle)(this.state.dataset[1]),
            this.state.yScale3d.rotateY(beta + this.startAngle).rotateX(alpha - this.startAngle)(this.state.dataset[2]),
            this.state.zScale3d.rotateY(beta + this.startAngle).rotateX(alpha - this.startAngle)(this.state.dataset[3])
        ];
        // Redraw plot
        this.drawPlot(data, 0);
    }

    // Hard coded for now
    loadWeights(data) {
        let lines = [];
        let nodes = [];

        for (let i = 0; i < data.length; i++) {
            let tokens = data[i];
            let pointX = parseFloat(tokens[0]);
            let pointY = parseFloat(tokens[1]);
            let pointZ = parseFloat(tokens[2]);
            // Append float data to list
            nodes.push({ x: pointX, y: pointY, z: pointZ });
        }

        for (let i = 0; i < data.length; i++) {
            let center = nodes[i];
            if (i % this.state.somWidth == this.state.somWidth - 1) {
                // At the right most column
                if (i != data.length - 1) {
                    // Not at the bottom row yet
                    let down = nodes[i + this.state.somWidth];
                    lines.push([center, down]); // Define line to the down node
                }
            } else if (Math.floor(i / this.state.somWidth) == this.state.somHeight - 1) {
                // At the bottom row
                let right = nodes[i + 1];
                lines.push([center, right]); // Define line to the right node
            } else {
                // Not at the bottom row nor at the right most column
                let down = nodes[i + this.state.somWidth];
                let right = nodes[i + 1];
                lines.push([center, down]); // Define line to the down node
                lines.push([center, right]); // Define line to the right node
            }
        }
        return [nodes, lines];
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
    importDataFile() {
        window.pywebview.api.open_csv_file().then((d) => {
            this.setState({ vizData: d[1], hasDataset: true, datasetName: d[0], showTraining: false, dataset: this.loadData(d[1]) }, () => {
                this.updatePlot();
            });
        });
    }

    // To accept a weights file from the upload point on ScatterView
    // TODO: this function is kept for to remaind compatible, might be removed since load was done in python
    importWeightsFile() {
        window.pywebview.api.open_json_file().then((d) => {
            let jsonData = d.weightspb;
            let weightData = this.loadWeights(jsonData);
            // console.log(jsonData)
            // TODO: update this.state.somHeight, this.state.somWidth as well when loading weights from JSON file
            this.setState({
                
                trainingData: jsonData,
                hasTraining: true, showTraining: true,
                weightsId: 0, weights: weightData[0], edges: weightData[1],
                somHeight: d.h, somWidth: d.w
            }, () => {
                this.updatePlot();
            });
        });
    }

    // Draws the scatter points and 3 axes
    drawPlot(result, tt) {
        console.log("drawing plot");
        this.drawPoints(result[0], tt);
        if (this.state.showTraining) {
            this.drawEdges(result[1]);
        } else {
            this.svg.selectAll("line").remove();
        }
        this.drawAxis(result[2], 'x', this.state.xScale3d);
        this.drawAxis(result[3], 'y', this.state.yScale3d);
        this.drawAxis(result[4], 'z', this.state.zScale3d);
    }

    // Function to update the current plot and redraw, created for slider feature when moving between plots
    updatePlot() {
        let result = [
            this.state.point3d(this.state.showTraining ? this.state.weights : this.state.dataset[0]),
            this.state.weights3d(this.state.edges),
            this.state.xScale3d(this.state.dataset[1]),
            this.state.yScale3d(this.state.dataset[2]),
            this.state.zScale3d(this.state.dataset[3]),
        ];
        this.drawPlot(result, 0);
    }

    // Define the svg variable, function to be used when initialising new state or restoring old state
    updateSvg() {
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
    }

    initView() {
        // Initialise d3 objects
        this.updateSvg();
        // Data points
        this.state.point3d = _3d()
            .x(function (d) { return d.x; })
            .y(function (d) { return -d.y; })
            .z(function (d) { return d.z; })
            .origin(this.origin)
            .rotateY(this.startAngle)
            .rotateX(-this.startAngle)
            .scale(this.scale);

        // Weight edges
        this.state.weights3d = _3d()
            .shape('LINE')
            .x(function (d) { return d.x; })
            .y(function (d) { return -d.y; })
            .z(function (d) { return d.z; })
            .origin(this.origin)
            .rotateY(this.startAngle)
            .rotateX(-this.startAngle)
            .scale(this.scale);

        // X axis
        this.state.xScale3d = _3d()
            .shape('LINE_STRIP')
            .origin(this.origin)
            .rotateY(this.startAngle)
            .rotateX(-this.startAngle)
            .scale(this.scale);

        // Y axis
        this.state.yScale3d = _3d()
            .shape('LINE_STRIP')
            .origin(this.origin)
            .rotateY(this.startAngle)
            .rotateX(-this.startAngle)
            .scale(this.scale);

        // Z axis
        this.state.zScale3d = _3d()
            .shape('LINE_STRIP')
            .origin(this.origin)
            .rotateY(this.startAngle)
            .rotateX(-this.startAngle)
            .scale(this.scale);
    }

    // Updates the origin and scale of d3 objects according to adjusted window size
    updateObjects() {
        // Data points
        this.state.point3d.origin(this.origin).scale(this.scale);
        // Weight points
        this.state.weights3d.origin(this.origin).scale(this.scale);
        // X axis
        this.state.xScale3d.origin(this.origin).scale(this.scale);
        // Y axis
        this.state.yScale3d.origin(this.origin).scale(this.scale);
        // Z axis
        this.state.zScale3d.origin(this.origin).scale(this.scale);
    }

    // Reads in adjusted window size to calculate origin and scale of d3 objects
    updateWindow() {
        let innerWidth = window.innerWidth - 180;
        let innerHeight = (window.innerHeight - 80) * 0.9;
        // Calculate origin and scale based on current window size
        this.origin = [innerWidth / 2, innerHeight / 2];
        this.scale = innerWidth / 620 > innerHeight / 480 ? innerHeight / 480 * 100 : innerWidth / 620 * 100;
        // Update d3 objects to be centered and scaled to new values
        this.updateObjects();
        // Redraw plot if the plot exists
        if (this.state.hasDataset) this.updatePlot();
    }

    // Function to update state on whether to show SOM training data or not based on switch
    handleShowTrainingChange() {
        this.setState((state) => {
            return { showTraining: !state.showTraining }
        }, () => this.updatePlot());
    }

    // Function to update state on which set of weights from the training process we should visualise
    handleWeightsIdChange(key) {
        return (value) => this.setState({
            [key]: value,
            weights: this.loadWeights(this.state.trainingData[value])[0],
            edges: this.loadWeights(this.state.trainingData[value])[1]
        }, () => this.updatePlot());
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
                        {this.state.hasDataset ?
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
                        <Button icon="one-to-many" disabled={!this.state.hasDataset} onClick={() => this.importWeightsFile()}>Train data</Button>
                    </ButtonGroup>


                </div>

                <div className="graph-area">
                    <svg className="scatterview-svg-render" ref={this.d3view} />
                    {this.state.trainingData == null ? <></> :
                        <div className="slider">
                            <Slider
                                disabled={!this.state.showTraining}
                                min={0}
                                max={Object.keys(this.state.trainingData).length} // This is hardcoded for now, TODO: JSON file need to include size 
                                stepSize={1}
                                labelStepSize={1}
                                onChange={this.handleWeightsIdChange("weightsId")}
                                value={this.state.weightsId}
                            />
                        </div>
                    }
                </div>


            </>)

    }
}

export default ScatterView3D;
