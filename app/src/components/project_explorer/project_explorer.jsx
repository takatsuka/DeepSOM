
import * as React from 'react'
import { Component } from 'react';

import { Classes, Icon, Intent, MenuDivider, TreeNodeInfo, Tree, Elevation, Card, Button, ButtonGroup, Dialog, MenuItem, ContextMenu, Menu } from "@blueprintjs/core";
import { Suggest } from "@blueprintjs/select";
import { Classes as Popover2Classes, ContextMenu2, Tooltip2 } from "@blueprintjs/popover2";
import { TAG_INPUT_VALUES } from '@blueprintjs/core/lib/esm/common/classes';

import DragDropSOM from '../drag-drop/drag-drop';
import ImageView from '../imageview/imageview';
import ScatterView3D from '../scatterview_3d/scatterview';

import { PrimaryToaster } from '../common/toaster';
import { INTENT_SUCCESS } from '@blueprintjs/core/lib/esm/common/classes';

class ProjectExplorer extends Component {
    constructor(props) {
        super(props)

        this.state = {
            workspaceName: "new",
            tree: [
                {
                    id: 0,
                    isExpanded: false,
                    icon: "folder-close",
                    label: 'Objects',
                    childNodes: []
                },
                {
                    id: 1,
                    isExpanded: false,
                    icon: "folder-close",
                    label: 'Models',
                    childNodes: []
                },
            ],

            data_picker: false,

            dp_type: "",
            dp_msg: "what the f?",
            dp_query: "",
            dp_items: [],
            dp_cb: null
        }
    }

    componentDidMount() {

    }

    refresh() {
        window.pywebview.api.call_service(this.props.datastore, "current_workspace_name", []).then((e) => {
            this.setState({
                workspaceName: e
            });
        });

        window.pywebview.api.call_service(this.props.datastore, "fetch_objects", ["matrix"]).then((e) => {
            let l = e.map((e, id) => ({
                id: { "type": "matrix", "key": e },
                hasCaret: false,
                icon: "database",
                label: e,
            }))

            this.state.tree[0].childNodes = l
            this.setState({ tree: this.state.tree })
        });

        window.pywebview.api.call_service(this.props.datastore, "fetch_objects", ["model"]).then((e) => {
            let l = e.map((e, id) => ({
                id: { "type": "model", "key": e },
                hasCaret: false,
                icon: "layout-auto",
                label: e,
            }))

            this.state.tree[1].childNodes = l
            this.setState({ tree: this.state.tree })
        });
    }

    loadWorkspace() {
        window.pywebview.api.call_service(this.props.datastore, "load_workspace", []).then(() => {
            this.refresh()
        })
    }

    createNewWorkspace() {
        window.pywebview.api.call_service(this.props.datastore, "new_workspace", []).then((e) => {
            this.refresh()
        });
    }

    saveWorkspace() {
        window.pywebview.api.call_service(this.props.datastore, "save_current_workspace", []).then((name) => {
            this.refresh()
        });
    }

    importData() {
        window.pywebview.api.call_service(this.props.datastore, "import_data_from_csv", []).then(() => {
            this.refresh()
        });
    }

    addSOM() {
        window.pywebview.api.call_service(this.props.datastore, "import_model", []).then((descriptor) => {
            if (descriptor == null) {
                return;
            }
            let newInstance = {
                icon: "polygon-filter",
                label: descriptor,
            }
            this.state.tree[0].childNodes.push(newInstance);
            this.setState((state) => {
                return { tree: state.tree };
            });
        });
    }

    newSOM(open) {
        window.pywebview.api.call_service(this.props.datastore, "save_object", ["SOM", "model", null, false]).then((descriptor) => {
            this.refresh()
            if (open) {
                this.props.openTab(<DragDropSOM />, descriptor, true, descriptor)
            }
        });

    }

    updateTree(thing) {
        thing()
        this.setState({ tree: this.state.tree })
    }

    handleOpen(item) {
        if (item.id.type === "model") {
            this.props.openTab(<DragDropSOM />, item.id.key, true, item.id.key)
        }
    }

    handleDelete(item) {
        if (item.id.key === null) return

        window.pywebview.api.call_service(this.props.datastore, "remove_object", [item.id.key]).then((descriptor) => {
            this.refresh()
        });
    }

    handleCtxMenu(item, p, e) {
        // if (item.icon === "folder-close") return
        e.preventDefault()
        console.log(item)
        let menu = (
            <Menu>
                <MenuDivider title={item.label} />
                <MenuItem icon="paperclip" text="Rename" />
                <MenuItem icon="trash" intent={Intent.DANGER} text="Delete" onClick={() => this.handleDelete(item)} />
            </Menu>
        )

        ContextMenu.show(menu, { left: e.clientX, top: e.clientY });

        return false
    }

    ask_user_pick_data(message, type, finish) {

        window.pywebview.api.call_service(this.props.datastore, "fetch_objects", [type]).then((e) => {
            this.setState({
                data_picker: true,
                dp_type: type,
                dp_msg: message,
                dp_items: e,
                dp_cb: finish
            })
        });

    }

    dpHandleClick(e) {
        console.log(e)
    }

    dpConfirm() {
        this.state.dp_cb(this.state.dp_query)
        this.setState({ data_picker: false })
    }

    render() {

        return (
            <>
                <ButtonGroup minimal={false} elevation={Elevation.FOUR} fill={true} alignText="left" minimal={true} large={true}>
                    <Button active={true} >{this.state.workspaceName}</Button>

                </ButtonGroup>

                <Dialog isOpen={this.state.data_picker} title="Select a data" onClose={() => this.setState({ data_picker: false })}>
                    <div className={Classes.DIALOG_BODY}>
                        <p>
                            <strong>
                                {this.state.dp_msg}
                            </strong>
                        </p>
                        <Suggest

                            inputValueRenderer={(e) => (e)}
                            itemRenderer={(e, { handleClick }) => <MenuItem key={e} text={e} onClick={handleClick} />}
                            items={this.state.dp_items}
                            onItemSelect={(e) => this.setState({ dp_query: e })}
                            popoverProps={{ minimal: true }}
                            query={this.state.dp_query}
                            onQueryChange={(q) => { this.setState({ dp_query: q }) }}
                            itemPredicate={(a, b) => b.toLowerCase().includes(a.toLowerCase())}
                            noResults={<MenuItem disabled={true} text="No results. Maybe import them first?" />}
                        />

                        <div className={Classes.DIALOG_FOOTER}>
                            <div className={Classes.DIALOG_FOOTER_ACTIONS}>

                                <Button onClick={() => this.setState({ data_picker: false })}>Cancel</Button>
                                <Button intent={Intent.SUCCESS} onClick={() => this.dpConfirm()}>Confirm</Button>

                            </div>
                        </div>
                    </div>
                </Dialog>

                <Tree elevation={Elevation.FOUR}
                    onNodeExpand={(x) => (this.updateTree(() => x.isExpanded = true))}
                    onNodeCollapse={(x) => (this.updateTree(() => x.isExpanded = false))}
                    contents={this.state.tree}
                    onNodeClick={this.handleOpen.bind(this)}
                    onNodeContextMenu={this.handleCtxMenu.bind(this)}

                />


            </>)

    }
}

export default ProjectExplorer;
