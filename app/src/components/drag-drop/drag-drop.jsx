import * as React from 'react'
import { Component } from 'react';
import Xarrow from "react-xarrows";

import { Label, Popover, Collapse, MenuDivider, ProgressBar, TextArea, InputGroup, Menu, Icon, NumericInput, Button, ButtonGroup, Card, Elevation, Alignment, Text, Dialog, Position, MenuItem, Divider, Drawer, DrawerSize, Classes, Portal, Intent } from "@blueprintjs/core";

import { ContextMenu2 } from "@blueprintjs/popover2";
import "./drag-drop.scss"
import { some } from 'd3-array';
import { timeHours } from 'd3-time';

import { PrimaryToaster } from '../common/toaster';
import { INTENT_SUCCESS } from '@blueprintjs/core/lib/esm/common/classes';

import { NodeTemplates } from './nodes'
import teacher from './imgs/training.gif';


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

            service: null,
            training: false
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


        this.node_templates = NodeTemplates

        if (window.pywebview)
            window.pywebview.api.launch_service("ModelService").then((x) => (
                this.setState({
                    service: x
                })
            ))

        var init = this.props.pullInit()
        if (init != null && window.pywebview !== null) {

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
        this.links = this.links.filter(l => !(l.from === id || l.to === id))
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

    compileModel() {
        console.log(this.state.service)
        window.pywebview.api.call_service(this.state.service, "update_model", [this.export_som()]).then((e) => {
            window.pywebview.api.call_service(this.state.service, "compile", []).then((e) => {
                PrimaryToaster.show({
                    message: e.status ? "Model compiled successfully." : "Failed: " + e.msg,
                    intent: e.status ? Intent.SUCCESS : Intent.DANGER,
                });
            });
        });

    }

    trainModel() {
        this.setState({training: true})
        window.pywebview.api.call_service(this.state.service, "train", []).then((e) => {
            this.setState({training: false})
            PrimaryToaster.show({
                message: e.status ? "Model training finished." : "Failed: " + e.msg,
                intent: e.status ? Intent.SUCCESS : Intent.DANGER,
            });
        });
    }

    pickInput() {
        this.props.fileman.ask_user_pick_data("Select a data to use for training.", "matrix", (k) => {
            console.log(k)
            window.pywebview.api.call_service(this.state.service, "set_input", [k]).then((e) => {
                PrimaryToaster.show({
                    message: "Training data set to: " + e.msg,
                    intent: Intent.SUCCESS
                });
            });
        })

    }

    saveGraphOutput() {
        window.pywebview.api.call_service(this.state.service, "export_output", [this.state.model_name+"_out"]).then((e) => {
            PrimaryToaster.show({
                message: (e.status ? "Exported as: "  : "Failed: ") + e.msg,
                intent: e.status ? Intent.SUCCESS : Intent.DANGER,
            });
            this.props.fileman.refresh()
        });
    }

    debugShowOutput() {
        window.pywebview.api.call_service(this.state.service, "debug_output_str", []).then((e) => {
            PrimaryToaster.show({
                message: (e.status ? ":"  : "Failed: ") + e.msg,
                intent: e.status ? Intent.PRIMARY : Intent.DANGER,
            });
            this.props.fileman.refresh()
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
                <MenuItem icon="add-to-artifact" text="Input Data" onClick={() => this.pickInput()} />
                <MenuDivider title="Action" />
                <MenuItem icon="ungroup-objects" text="Compile" onClick={() => this.compileModel()} />
                <MenuItem icon="repeat" text="Train" onClick={() => this.trainModel()} />
                <MenuDivider title="Result" />
                <MenuItem icon="play" text="Save Output" onClick={() => this.saveGraphOutput()} />
                <MenuDivider title="Debug" />
                <MenuItem icon="database" text="Show Output" onClick={() => this.debugShowOutput()} />

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
                                <Button icon="help" intent="success" minimal disabled> Open Manual </Button>
                            </div>
                        </Drawer>
                    </div>


                    <Dialog isOpen={this.state.training} title="Training in progress" icon="data-lineage" isCloseButtonShown={false}>
                        <div className={Classes.DIALOG_BODY}>
                            <p>
                                <strong>
                                    Grab a coffee, this won't take long. ☕️
                                    <br />
                                </strong>
                            </p>
                            <ProgressBar intent={Intent.PRIMARY} />
                            <p style={{ marginTop: "15px" }}>
                                To reduce potential bugs, the application will not respond until this is completed.
                            </p>
                            <p style={{ marginTop: "15px" }}>
                                Taking too long? We apologize, if you believe something went wrong please force quit and restart the application.
                                As stated in our license, we are not responsible for any data loss.
                            </p>
                            <img src={teacher} style={{marginLeft:'90px'}} height={250}/>
                        </div>
                    </Dialog>

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
