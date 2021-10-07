import * as React from 'react'
import { Component } from 'react';
import Xarrow from "react-xarrows";

import { Label, Popover, Collapse, TextArea, InputGroup, Menu, Icon, NumericInput, Button, ButtonGroup, Card, Elevation, Alignment, Text, Position, MenuItem, Divider, Drawer, DrawerSize, Classes, Portal } from "@blueprintjs/core";

import { ContextMenu2 } from "@blueprintjs/popover2";
import "./drag-drop.scss"
import { some } from 'd3-array';
import { timeHours } from 'd3-time';

class DragDropSOM extends Component {
    constructor(props) {
        super(props);
        this.state = { dragging: false };
        this.onMouseMove = this.onMouseMove.bind(this);
        this.onMouseUp = this.onMouseUp.bind(this);
    }

    onMouseDown(e) {
        // console.log("DOWN");
        if (e.buttons !== 1) return
        this.setState({
            dragging: true, prev_mouse_pos: {
                x: event.pageX,
                y: event.pageY
            }
        });
        document.addEventListener('mousemove', this.onMouseMove);
        document.addEventListener('mouseup', this.onMouseUp);
    }

    onMouseUp() {
        // console.log("UP");
        this.setState({ dragging: false });
        document.removeEventListener('mousemove', this.onMouseMove);
        document.removeEventListener('mouseup', this.onMouseUp);
    }

    onMouseMove(e) {
        if (!this.state.dragging) return
        var n = this.props.node
        var current_mouse_pos = {
            x: e.pageX,
            y: e.pageY
        };
        var new_x = n.x + current_mouse_pos.x - this.state.prev_mouse_pos.x;
        var new_y = n.y + current_mouse_pos.y - this.state.prev_mouse_pos.y;
        this.setState({ prev_mouse_pos: current_mouse_pos });
        this.props.parent.child_update(n.id, Math.round(new_x), Math.round(new_y));
    }

    contextMenu(e) {
        e.preventDefault()
        this.props.parent.openSideMenu(this)
    }

    render() {
        var n = this.props.node
        var t = this.props.template
        var s = t.style

        return (
            <div className="dd-som" id={"ddn_" + n.id}
                style={{ top: n.y, left: n.x, opacity: this.state.dragging ? 0.6 : 1, width: s.width, height: s.height }}
                onMouseDown={this.onMouseDown.bind(this)}
                onContextMenu={this.contextMenu.bind(this)}
            >

                <Card style={{ backgroundColor: s.backgroundColor, width: s.width, height: s.height }} interactive={true} elevation={Elevation.THREE}>
                    {t.render(n)}
                    {this.props.parent.state.add_link_active ? (
                        <Button icon="add" intent="success" onClick={() => this.props.parent.add_link_node(n.id)} />
                    ) : (
                        <></>
                    )}
                </Card>

            </div>
        );
    }
}

class DragDrop extends Component {
    constructor(props) {
        super(props)
        this.state = {
            soms: {

            },
            add_link_active: false,
            add_link_step: 1,
            advanced_open: false,
            side_menu: false,
            editing: null
        };

        // Bind functions
        this.add_som = this.add_som.bind(this);
        this.add_link_init = this.add_link_init.bind(this);
        this.add_link_cancel = this.add_link_cancel.bind(this);
        this.add_link_node = this.add_link_node.bind(this);
        this.render = this.render.bind(this);
        this.remove_handler = this.remove_handler.bind(this);
        this.child_update = this.child_update.bind(this);
        this.advanced_toggle = this.advanced_toggle.bind(this);
        this.import_som = this.import_som.bind(this);

        this.new_link_nodes = [-1, -1];
        this.links = [];
        this.i = 0;


        this.node_templates = {
            inout: {
                name: "Input",
                fixed: true,
                style: { backgroundColor: "#738694", width: "100px", height: "100px" },
                node_props: { dim: 3 },
                render: (d) => (
                    <div style={{ textAlign: 'center' }}>
                        <p style={{ fontSize: '18px' }}>{d.name}</p>
                        <strong style={{}}>{d.props.dim}</strong>
                    </div>
                ),

                contextMenu: (d) => (
                    <div>
                        <InputGroup placeholder="Name" disabled value={d.name} onChange={(t) => this.wrapSOMS(() => (d.name = t.target.value))} />
                        <Divider />
                        <NumericInput
                            value={d.props.dim} onValueChange={(t) => this.wrapSOMS(() => (d.props.dim = t))}
                            rightElement={<Button disabled minimal>Dimension</Button>}
                            fill buttonPosition="left" placeholder="10" />
                    </div>
                )
            },

            get_bmu: {
                name: "get_bmu_",
                style: { backgroundColor: "#D9822B", width: "180px", height: "50px" },
                node_props: { shape: '2d_dis' },
                render: (d) => (
                    <div style={{ textAlign: 'center', marginTop: "-7px" }}>
                        <i style={{ fontSize: '18px' }}>Get BMU({d.props.shape})</i>
                    </div>
                ),

                contextMenu: (d) => (
                    <div>
                        <InputGroup placeholder="Name" value={d.name} onChange={(t) => this.wrapSOMS(() => (d.name = t.target.value))} />
                        <Divider />
                        <InputGroup placeholder="rect" value={d.props.shape} onChange={(t) => this.wrapSOMS(() => (d.props.shape = t.target.value))} />
                    </div>
                )
            },

            som: {
                name: "SOM",
                style: { backgroundColor: "#137CBD", width: "200px", height: "200px" },
                node_props: { dim: 10, shape: 'rect', inputDim: 3 },
                render: (d) => (
                    <div style={{ textAlign: 'center' }}>

                        <p style={{ fontSize: '18px' }}>{d.name}</p>
                        <Icon icon="layout-grid" size={30} />

                        <div style={{ textAlign: 'left', marginTop: "20px" }}>
                            <strong style={{}}> Dimension:</strong><br />
                            <div style={{ paddingLeft: "10px", marginBottom: '10px' }}>
                                Data: {d.props.inputDim} <br />
                                Internal: {d.props.dim}
                            </div>
                            <strong style={{}}> Shape: </strong> {d.props.shape}<br />
                        </div>

                    </div>
                ),
                contextMenu: (d) => (
                    <div>
                        <InputGroup placeholder="Name" value={d.name} onChange={(t) => this.wrapSOMS(() => (d.name = t.target.value))} />
                        <Divider />
                        <NumericInput
                            value={d.props.dim} onValueChange={(t) => this.wrapSOMS(() => (d.props.dim = t))}
                            rightElement={<Button disabled minimal>Dimension</Button>}
                            fill buttonPosition="left" placeholder="10" />
                        <NumericInput
                            value={d.props.inputDim} onValueChange={(t) => this.wrapSOMS(() => (d.props.inputDim = t))}
                            rightElement={<Button disabled minimal>Input Dimension</Button>}
                            fill buttonPosition="left" placeholder="10" />
                        <InputGroup placeholder="rect" value={d.props.shape} onChange={(t) => this.wrapSOMS(() => (d.props.shape = t.target.value))} />
                    </div>
                )
            },

            sampler: {
                name: "Sampler",
                style: { backgroundColor: "#DB2C6F", width: "190px", height: "140px" },
                node_props: { dim: 100 },
                render: (d) => (
                    <div style={{ textAlign: 'center' }}>

                        <p style={{ fontSize: '18px' }}>{d.name}</p>
                        <Icon icon="heat-grid" size={30} />

                        <div style={{ textAlign: 'left', marginTop: "20px" }}>
                            <p style={{}}> Input Patches: {d.props.dim}</p><br />
                        </div>

                    </div>
                ),
                contextMenu: (d) => (
                    <div>
                        <InputGroup placeholder="Name" value={d.name} onChange={(t) => this.wrapSOMS(() => (d.name = t.target.value))} />
                        <Divider />
                        <NumericInput
                            value={d.props.dim} onValueChange={(t) => this.wrapSOMS(() => (d.props.dim = t))}
                            rightElement={<Button disabled minimal>N Patches</Button>}
                            fill buttonPosition="left" placeholder="10" />

                    </div>
                )
            },

            minipatch: {
                name: "mini patcher",
                style: { backgroundColor: "#00B3A4", width: "190px", height: "185px" },
                node_props: { dim: 100, kernel: 10, stride: 2 },
                render: (d) => (
                    <div style={{ textAlign: 'center' }}>

                        <p style={{ fontSize: '18px' }}>{d.name}</p>
                        <Icon icon="multi-select" size={30} />

                        <div style={{ textAlign: 'left', marginTop: "5px" }}>
                            <strong style={{}}> Format:</strong><br />
                            <div style={{ paddingLeft: "10px", marginBottom: '10px' }}>
                                Kernel: {d.props.kernel} <br />
                                Strides: {d.props.stride}
                            </div>
                            <strong style={{}}> N Input: </strong> {d.props.dim}<br />
                        </div>

                    </div>
                ),
                contextMenu: (d) => (
                    <div>
                        <InputGroup placeholder="Name" value={d.name} onChange={(t) => this.wrapSOMS(() => (d.name = t.target.value))} />
                        <Divider />
                        <NumericInput
                            value={d.props.kernel} onValueChange={(t) => this.wrapSOMS(() => (d.props.kernel = t))}
                            rightElement={<Button disabled minimal>Kernel</Button>}
                            fill buttonPosition="left" placeholder="10" />
                        <NumericInput
                            value={d.props.stride} onValueChange={(t) => this.wrapSOMS(() => (d.props.stride = t))}
                            rightElement={<Button disabled minimal>Strides</Button>}
                            fill buttonPosition="left" placeholder="10" />

                        <NumericInput
                            value={d.props.dim} onValueChange={(t) => this.wrapSOMS(() => (d.props.dim = t))}
                            rightElement={<Button disabled minimal>N Input</Button>}
                            fill buttonPosition="left" placeholder="10" />

                    </div>
                )
            }
        }

        var restored = this.props.pullState()

        if(restored != null && "state" in restored && "links" in restored){
            this.links = restored.links
            this.state = restored.state
            this.i = restored.i
            return
        }

        var input = this.create_som("inout")
        input.x = 100
        input.y = 200
        input.name = "Input"
        this.state.soms[input.id] = input

        var output = this.create_som("inout")
        output.x = 600
        output.y = 200
        output.name = "Output"
        output.props.dim = 2
        this.state.soms[output.id] = output

    }

    componentWillUnmount() {
        this.props.saveState({state: this.state, links: this.links, i: this.i})
    }

    wrapSOMS(thing) {
        thing()
        this.setState({ soms: this.state.soms })
    }

    create_som(template) {

        var te = this.node_templates[template]
        var newN = {}
        newN.name = te.name
        newN.id = (++this.i)
        newN.x = Math.round(Math.random() * 800);
        newN.y = Math.round(Math.random() * 600);
        newN.props = JSON.parse(JSON.stringify(te.node_props))
        newN.template = template

        return newN
    }

    add_som(template) {

        var node = this.create_som(template)
        this.state.soms[this.i] = node;
        this.setState({ soms: this.state.soms });

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
        var s = this.state.soms
        delete s[id]
        this.setState({ soms: s, side_menu: false, editing: null });
    }

    child_update(id, x, y) {
        this.state.soms[id].x = x;
        this.state.soms[id].y = y;
        this.setState({ render_now: true });
    }

    advanced_toggle() {
        this.setState({ advanced_open: !this.state.advanced_open });
    }

    import_som(e) {
        const data = JSON.parse(event.target.value);
        this.links = data['links'];
        this.setState({ soms: data['soms'] });
    }

    export_som() {
        return { nodes: this.state.soms, connections: this.links }
    }

    closeSideMenu() {
        this.setState({ side_menu: false, editing: null })
    }

    openSideMenu(som) {
        this.setState({ side_menu: true, editing: som.props.node.id })
    }

    saveSession() {
        window.pywebview.api.save_json_file(this.export_som()).then((e) => (console.log(e)))
    }

    loadSessionFromFile() {
        window.pywebview.api.open_json_file().then(function (x) {
            this.links = x.connections
            this.setState({ soms: x.nodes })
        }.bind(this))
    }

    render() {
        const add_som_enable = true;
        const add_link_active = this.state.add_link_active;
        const add_link_step = this.state.add_link_step;
        const this_obj = this;

        let add_link_content = (
            <div>
                {add_link_step == 1 ? (
                    <h3>Select first node</h3>
                ) : (
                    <h2>Select second node</h2>
                )}
            </div>
        );

        var editingNode = this.state.soms[this.state.editing]

        const sessionMenu = (
            <Menu>
                <MenuItem icon="document-share" text="Save" onClick={() => this.saveSession()} />
                <MenuItem icon="document-open" text="Load" onClick={() => this.loadSessionFromFile()} />
            </Menu>
        )

        const addMenu = (
            <Menu>
                <MenuItem icon="one-to-many" text="Distributor" />
                <MenuItem icon="many-to-one" text="Concatenator" />
                <Divider />
                <MenuItem icon="layout-skew-grid" text="Single SOM" onClick={() => this.add_som("som")} />
                <MenuItem icon="heat-grid" text="Sampler" onClick={() => this.add_som("sampler")} />
                <MenuItem icon="new-grid-item" text="Mini Patcher" onClick={() => this.add_som("minipatch")} />
                <Divider />
                <MenuItem icon="function" text="Get BMU" onClick={() => this.add_som("get_bmu")} />
                <MenuItem icon="function" text="Random Sample" />


            </Menu>
        )

        return (
            <>

                <div className="submenu">

                    <ButtonGroup style={{ minWidth: 200 }} minimal={true} className="sm-buttong">
                        <Button disabled={true} >not_so_deep_som</Button>
                        <Divider />
                        <Popover content={sessionMenu} position={Position.BOTTOM_LEFT} interactionKind="click">
                            <Button className="bp3-minimal" icon="code-block" text="Session" />
                        </Popover>

                        <Divider />

                        <Popover content={addMenu} position={Position.BOTTOM_LEFT} interactionKind="click">
                            <Button icon="add" text="Add Node" />
                        </Popover>

                        <Popover content={add_link_content} popoverClassName="bp3-popover-content-sizing" onClose={this.add_link_cancel} interactionKind="CLICK_TARGET_ONLY" isOpen={add_link_active} >
                            <Button icon="new-link" text="Add Link" onClick={this.add_link_init} active={add_link_active} />
                        </Popover>

                        <Button icon="cog" onClick={this.advanced_toggle}>
                            {this.state.advanced_open ? "Hide" : "Show"} Advanced Options
                        </Button>
                    </ButtonGroup>
                    <Collapse isOpen={this.state.advanced_open}>
                        <Icon icon="export" /> Export SOM
                        <TextArea id="export_som" value={JSON.stringify({ "soms": this.state.soms, "links": this.links })} growVertically={true} />
                        <Icon icon="import" /> Import SOM
                        <TextArea id="import_som" growVertically={true} onChange={this.import_som} />
                    </Collapse>
                </div>


                <div className="drag-drop-box">
                    <div className="dd-submenu">

                        <Drawer

                            icon="info-sign"
                            onClose={() => (this.closeSideMenu())}
                            title="Properties"
                            size={DrawerSize.SMALL}
                            usePortal={true}
                            isOpen={this.state.side_menu}
                            hasBackdrop={false}
                            style={{ marginTop: "145px", marginRight: "20px", marginBottom: "20px" }}
                        >
                            <div className={Classes.DRAWER_BODY}>
                                <div className={Classes.DIALOG_BODY}>

                                    {this.state.editing == null ? <></> : this.node_templates[editingNode.template].contextMenu(editingNode)}

                                </div>
                            </div>
                            <div className={Classes.DRAWER_FOOTER}>
                                <Button icon="trash" intent="danger" disabled={editingNode && 'fixed' in this.node_templates[editingNode.template]} minimal onClick={() => this.remove_handler(this.state.editing)}> Delete </Button>
                                <Button icon="help" intent="success" minimal> Open Manual </Button>
                            </div>
                        </Drawer>
                    </div>


                    <div className="som-box" id="som-box">
                        {Object.keys(this.state.soms).map(function (k, idx) {
                            var d = this.state.soms[k]
                            return (<DragDropSOM key={d.id} node={d} template={this.node_templates[d.template]} parent={this_obj} />);
                        }.bind(this))}
                        {this.links.map(function (d, idx) {
                            return (<Xarrow key={idx} start={"ddn_" + d[0]} end={"ddn_" + d[1]} dashness={{ animation: 0.5 }} />);
                        })}
                    </div>
                </div>
            </>
        );
    }
}

export default DragDrop;
