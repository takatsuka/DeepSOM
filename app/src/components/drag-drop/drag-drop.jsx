import * as React from 'react'
import { Component } from 'react';
import Xarrow from "react-xarrows";

import { Label, Popover, Collapse, MenuDivider, TextArea, InputGroup, Menu, Icon, NumericInput, Button, ButtonGroup, Card, Elevation, Alignment, Text, Position, MenuItem, Divider, Drawer, DrawerSize, Classes, Portal, Intent } from "@blueprintjs/core";

import { ContextMenu2 } from "@blueprintjs/popover2";
import "./drag-drop.scss"
import { some } from 'd3-array';
import { timeHours } from 'd3-time';

import { PrimaryToaster } from '../common/toaster';
import { INTENT_SUCCESS } from '@blueprintjs/core/lib/esm/common/classes';

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
            model_name: "?",
            soms: {

            },
            add_link_active: false,
            add_link_step: 1,
            advanced_open: false,
            side_menu: false,
            editing: null,

            service: null
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

            bypass: {
                name: "Identity",
                fixed: true,
                style: { backgroundColor: "#202B33", width: "50px", height: "50px" },
                node_props: { dim: 3 },
                render: (d) => (
                    <div style={{ textAlign: 'center', marginTop: "-9px", marginLeft: "-9px" }}>
                        <Icon icon="flow-linear" size={30} />
                    </div>
                ),

                contextMenu: (d) => (
                    <div>
                        <InputGroup placeholder="Name" disabled value={d.name} onChange={(t) => this.wrapSOMS(() => (d.name = t.target.value))} />
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

            dist: {
                name: "dist",
                style: { backgroundColor: "#00998C", width: "70px", height: "100px" },
                node_props: { selections: [{ type: "idx", sel: [0, 1] }], axis: 1 },
                render: (d) => (
                    <div style={{ textAlign: 'center', marginTop: "15px" }}>
                        <Icon icon="one-to-many" size={30} />
                    </div>
                ),

                updateInput: function (old, text) {
                    var n = text.split(",").map((a) => parseInt(a))
                    if (n.some((n) => isNaN(n))) return old

                    return n
                },

                contextMenu: (d) => (
                    <div>

                        <InputGroup placeholder="Name" value={d.name} onChange={(t) => this.wrapSOMS(() => (d.name = t.target.value))} />
                        <NumericInput
                            value={d.props.axis} onValueChange={(t) => this.wrapSOMS(() => (d.props.axis = t))}
                            rightElement={<Button disabled minimal>Axis</Button>}
                            fill buttonPosition="left" placeholder="10" />
                        <Divider />
                        {d.props === null ? <></> : d.props.selections.map(function (sel, idx) {
                            return (
                                <div key={idx}>
                                    <InputGroup placeholder="crap" value={d.props.selections[idx].sel}
                                        onChange={(t) => this.wrapSOMS(() => (d.props.selections[idx].sel = this.node_templates[d.template].updateInput(d.props.selections[idx].sel, t.target.value)))} />
                                </div>
                            )

                        }.bind(this))}


                        <ButtonGroup style={{ minWidth: 200 }} minimal={true} className="sm-buttong">
                            <Button icon="plus" intent="success"
                                onClick={() => this.wrapSOMS(() => (d.props.selections = [...d.props.selections, { type: "idx", sel: [0, 1] }]))}
                            >
                                Add
                            </Button>
                        </ButtonGroup>
                    </div>
                )
            },

            concat: {
                name: "concat",
                style: { backgroundColor: "#00998C", width: "70px", height: "100px" },
                node_props: { selections: [{ type: "idx", sel: [0, 1] }], axis: 1 },
                render: (d) => (
                    <div style={{ textAlign: 'center', marginTop: "15px" }}>
                        <Icon icon="many-to-one" size={30} />
                    </div>
                ),

                contextMenu: (d) => (
                    <div>

                        <InputGroup placeholder="Name" value={d.name} onChange={(t) => this.wrapSOMS(() => (d.name = t.target.value))} />
                        <NumericInput
                            value={d.props.axis} onValueChange={(t) => this.wrapSOMS(() => (d.props.axis = t))}
                            rightElement={<Button disabled minimal>Axis</Button>}
                            fill buttonPosition="left" placeholder="10" />
                        <Divider />
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

        window.pywebview.api.launch_service("ModelService").then((x) => (
            this.setState({
                service: x
            })
        ))

        var init = this.props.pullInit()
        if (init != null) {

            window.pywebview.api.call_service(-1, "get_object", [init]).then((e) => {
                if (e !== null) {
                    this.import_som(e)
                }
                else {
                    this.init_model(false)
                }

                this.setState({
                    model_name: init,
                    soms: this.state.soms
                })
            });

            return
        }

        var restored = this.props.pullState()

        if (restored != null && "state" in restored && "links" in restored) {
            this.links = restored.links
            this.state = restored.state
            this.i = restored.i
            return
        }


        this.init_model(false)


    }

    init_model(updateState) {
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
        if (updateState) this.setState({ soms: this.state.soms })
    }

    componentWillUnmount() {
        this.props.saveState({ state: this.state, links: this.links, i: this.i })
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

    push_link() {
        if (this.links.some(l => (l.from == this.new_link_nodes[0] && l.to == this.new_link_nodes[1]))) {
            PrimaryToaster.show({
                message: "Cannot add link - an identical link exists.",
                intent: Intent.DANGER,
            });

            return
        }

        var nl = {
            from: this.new_link_nodes[0],
            to: this.new_link_nodes[1],
            props: {
                slot: 0,
                order: 0
            }
        }
        this.links.push(nl);

        this.setState({ add_link_active: false, add_link_step: -1 });
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
            this.push_link()
        }
    }

    update_link_slot(lk, slot) {
        lk.props.slot = slot
        this.setState({}) // force render
    }

    remove_link(lk) {
        this.links = this.links.filter(l => (l.from !== lk.from && l.to !== lk.to))
        this.setState({}) // force render
    }

    links_for_node(id, out) {
        if (out) {
            return this.links.filter(l => l.from === id)
        }

        return this.links.filter(l => l.to === id)
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

    closeSideMenu() {
        this.setState({ side_menu: false, editing: null })
    }

    openSideMenu(som) {
        this.setState({ side_menu: true, editing: som.props.node.id })
    }

    import_som(x) {
        this.links = x.connections
        this.i = x.i
        this.setState({ soms: x.nodes })
    }

    export_som() {
        return {
            nodes: this.state.soms,
            connections: this.links,
            i: this.i
        }
    }

    saveSession() {
        window.pywebview.api.call_service(-1, "save_object", [this.state.model_name, "model", this.export_som(), true]).then((descriptor) => {
        });
    }

    loadSession() {

    }

    saveSessionToFile() {
        window.pywebview.api.save_json_file(this.export_som()).then((e) => (console.log(e)))
    }

    loadSessionFromFile() {
        window.pywebview.api.open_json_file().then(function (x) {
            this.import_som(x)
        }.bind(this))
    }

    trainModel(){
        console.log(this.state.service)
        window.pywebview.api.call_service(this.state.service, "compile", []).then((e) => {
            console.log(e)
        });
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
                    <h3>Select second node</h3>
                )}
            </div>
        );

        var editingNode = this.state.soms[this.state.editing]

        const sessionMenu = (
            <Menu>
                <MenuItem icon="document-share" text="Save" onClick={() => this.saveSession()} />
                <MenuDivider title="External" />
                <MenuItem icon="document-share" text="Save to file" onClick={() => this.saveSessionToFile()} />
                <MenuItem icon="document-open" text="Load from file" onClick={() => this.loadSessionFromFile()} />
            </Menu>
        )

        const runtimeMenu = (
            <Menu>
                <MenuItem icon="add-to-artifact" text="Input Data" disabled />
                <Divider />
                <MenuItem icon="ungroup-objects" text="Compile" disabled />
                <MenuItem icon="repeat" text="Train" onClick={() => this.trainModel()} />
                <Divider />
                <MenuItem icon="play" text="Save Output" disabled />
            </Menu>
        )

        const addMenu = (
            <Menu>
                <MenuItem icon="flow-linear" text="Bypass" onClick={() => this.add_som("bypass")} />
                <Divider />
                <MenuItem icon="one-to-many" text="Distributor" onClick={() => this.add_som("dist")} />
                <MenuItem icon="many-to-one" text="Concatenator" onClick={() => this.add_som("concat")} />
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
                        {/* <Button disabled={true} >not_so_deep_som</Button> */}
                        <Divider />
                        <Popover content={sessionMenu} position={Position.BOTTOM_LEFT} interactionKind="click">
                            <Button className="bp3-minimal" icon="code-block" text="Session" />
                        </Popover>

                        <Popover content={runtimeMenu} position={Position.BOTTOM_LEFT} interactionKind="click">
                            <Button className="bp3-minimal" icon="code-block" text="Runtime" />
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

                                    <h3>Fields:</h3>
                                    {this.state.editing == null ? <></> : this.node_templates[editingNode.template].contextMenu(editingNode)}

                                    <Divider />
                                    <h3>Incoming:</h3>
                                    {this.state.editing == null ? <></> : this.links_for_node(editingNode.id, false).map(function (l, idx) {
                                        let other = this.state.soms[l.from]
                                        console.log(other)
                                        return (
                                            <div key={idx} className="editor-edge-item">
                                                <p className="editor-edge-item-text">{other.name}</p>
                                                <div className="editor-edge-item-slot">
                                                    <NumericInput fill value={l.props.slot} onValueChange={(v) => this.update_link_slot(l, v)} />
                                                </div>

                                                <Button minimal icon="cross" intent={Intent.DANGER} onClick={() => this.remove_link(l)} />
                                            </div>
                                        )

                                    }.bind(this))}


                                    <Divider />
                                    <h3>Outgoing:</h3>
                                    {this.state.editing == null ? <></> : this.links_for_node(editingNode.id, true).map(function (l, idx) {
                                        let other = this.state.soms[l.to]
                                        console.log(other)
                                        return (
                                            <div key={idx} className="editor-edge-item">
                                                <p className="editor-edge-item-text">{other.name}</p>
                                                <div className="editor-edge-item-slot">
                                                    <NumericInput fill value={l.props.slot} onValueChange={(v) => this.update_link_slot(l, v)} />
                                                </div>

                                                <Button minimal icon="cross" intent={Intent.DANGER} onClick={() => this.remove_link(l)} />
                                            </div>
                                        )

                                    }.bind(this))}





                                    <Divider />
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
                            return (<Xarrow key={idx} start={"ddn_" + d.from} end={"ddn_" + d.to} dashness={{ animation: 0.5 }} />);
                        })}
                    </div>
                </div>
            </>
        );
    }
}

export default DragDrop;
