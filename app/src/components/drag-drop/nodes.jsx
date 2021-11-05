import * as React from 'react'
import { Component } from 'react';
import Xarrow from "react-xarrows";

import { Label, Popover, Collapse, MenuDivider, ProgressBar, TextArea, InputGroup, Menu, Icon, NumericInput, Button, ButtonGroup, Card, Elevation, Alignment, Text, Dialog, Position, MenuItem, Divider, Drawer, DrawerSize, Classes, Portal, Intent } from "@blueprintjs/core";



export const NodeTemplates = {

    inout: {
        name: "Input",
        fixed: true,
        styleClass: "inout_node",
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
        styleClass: "bypass_node",
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
        styleClass: "get_bmu_node",
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
        styleClass: "dist_node",
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
        styleClass: "concat_node",
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
        styleClass: "som_node",
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
        styleClass: "sampler_node",
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
        styleClass: "minipatch_node",
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
