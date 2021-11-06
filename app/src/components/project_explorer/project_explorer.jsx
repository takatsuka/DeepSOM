
import * as React from 'react'
import { Component } from 'react';

import { Classes, IconSize, Intent, MenuDivider, Tree, Elevation, Spinner, Button, ButtonGroup, Dialog, MenuItem, ContextMenu, Menu, InputGroup, Icon } from "@blueprintjs/core";
import { Example } from "@blueprintjs/docs-theme";
import { Suggest } from "@blueprintjs/select";

import DragDropSOM from '../drag-drop/drag-drop';
import ImageView from '../imageview/imageview';
import ScatterView3D from '../scatterview_3d/scatterview';

import { PrimaryToaster } from '../common/toaster';
import { INTENT_SUCCESS } from '@blueprintjs/core/lib/esm/common/classes';

class ProjectExplorer extends Component {
    constructor(props) {
        super(props)

        this.handleFilterChange = this.handleFilterChange.bind(this)

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
                {
                    id: 2,
                    isExpanded: false,
                    icon: "data-connection",
                    label: 'Opaques',
                    childNodes: []
                },
            ],

            data_picker: false,
            dp_type: "",
            dp_msg: "what the f?",
            dp_query: "",
            dp_items: [],
            dp_cb: null,

            rename: false,
            renameFrom: "",
            renameTo: "",

            objectInspector: false,
            objectDes: null
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

        window.pywebview.api.call_service(this.props.datastore, "fetch_objects", ["opaque"]).then((e) => {
            let l = e.map((e, id) => ({
                id: { "type": "opaque", "key": e },
                hasCaret: false,
                icon: "data-connection",
                label: e,
            }))

            this.state.tree[2].childNodes = l
            this.setState({ tree: this.state.tree })
        });
    }

    inspectObject(key) {
        window.pywebview.api.call_service(this.props.datastore, "fetch_object_repr", [key]).then((e) => {
            if(!e.status) {
                PrimaryToaster.show({
                    message: "Failed: " + e.msg,
                    intent: Intent.DANGER,
                });
            }
            
            this.setState({ objectInspector: true, objectDes: e })
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

    renameObject() {
        window.pywebview.api.call_service(-1, "rename_object", [this.state.renameFrom, this.state.renameTo]).then((e) => {

            this.setState({ rename: false }, () => {
                PrimaryToaster.show({
                    message: (e.status ? "Successfully renamed to: " : "Failed: ") + e.msg,
                    intent: e.status ? Intent.SUCCESS : Intent.DANGER,
                });
                this.refresh();
            })
        })
    }

    updateTree(thing) {
        thing()
        this.setState({ tree: this.state.tree })
    }

    handleOpen(item) {
        if (item.id.type === "model") {
            this.props.openTab(<DragDropSOM />, item.id.key, true, item.id.key)
        }

        if(item.id.type === "opaque") {
            this.inspectObject(item.id.key)
        }
    }

    handleDelete(item) {
        if (item.id.key === null) return

        window.pywebview.api.call_service(this.props.datastore, "remove_object", [item.id.key]).then((descriptor) => {
            this.refresh()
        });
    }

    handleRename(item) {
        this.setState({ rename: true, renameFrom: item.id.key, renameTo: item.id.key });
    }

    handleCtxMenu(item, p, e) {
        if (item.icon === "folder-close") return
        e.preventDefault()
        console.log(item)
        let menu = (
            <Menu>
                <MenuDivider title={item.label} />
                <MenuItem icon="paperclip" text="Rename" onClick={() => this.handleRename(item)} />
                <MenuItem icon="trash" intent={Intent.DANGER} text="Delete" onClick={() => this.handleDelete(item)} />
                <MenuDivider title="Advanced" />
                <MenuItem icon="data-connection" text="Inspect" onClick={() => this.inspectObject(item.id.key)} />
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

    handleFilterChange(key) {
        return (event) => this.setState({
            [key]: event.currentTarget.value,
            nameExists: false
        }, () => {
            window.pywebview.api.call_service(-1, "ensure_unique", [this.state.filterValue]).then((name) => {
                if (name.localeCompare(this.state.filterValue) != 0) {
                    this.setState({ nameExists: true })
                } else {
                    this.setState({ nameExists: false })
                }
            })
        })
    }



    render() {

        return (
            <>
                <ButtonGroup minimal={false} elevation={Elevation.FOUR} fill={true} alignText="left" minimal={true} large={true}>
                    <Button active={true} >{this.state.workspaceName}</Button>

                </ButtonGroup>

                <Dialog isOpen={this.state.rename} title="Rename" onClose={() => this.setState({ rename: false })}>
                    <div>
                        <div className={Classes.DIALOG_BODY}>
                            <Example>
                                <InputGroup
                                    onChange={(x) => this.setState({ renameTo: x.target.value })}
                                    value={this.state.renameTo}
                                />
                            </Example>
                            <div class=".bp3-ui-text">
                                <pre class="tab" color="red">
                                    {this.state.nameExists ? "Name already exists." : "        "}
                                </pre>
                            </div>

                        </div>
                        <div className={Classes.DIALOG_FOOTER}>
                            <div className={Classes.DIALOG_FOOTER_ACTIONS}>

                                <Button onClick={() => this.setState({ rename: false })}>Cancel</Button>
                                <Button intent={Intent.SUCCESS} disabled={this.state.nameExists} onClick={() => this.renameObject()}>Confirm</Button>

                            </div>
                        </div>
                    </div>
                </Dialog>

                <Dialog isOpen={this.state.data_picker} title="Select data" onClose={() => this.setState({ data_picker: false })}>
                    <div>
                        <div className={Classes.DIALOG_BODY}>
                            <p>
                                <strong>
                                    Type: {this.state.dp_msg}
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


                        </div>
                        <div className={Classes.DIALOG_FOOTER}>
                            <div className={Classes.DIALOG_FOOTER_ACTIONS}>

                                <Button onClick={() => this.setState({ data_picker: false })}>Cancel</Button>
                                <Button intent={Intent.SUCCESS} onClick={() => this.dpConfirm()}>Confirm</Button>

                            </div>
                        </div>
                    </div>
                </Dialog>

                <Dialog isOpen={this.state.objectInspector} title="Opaque Object Inspector" onClose={() => this.setState({ objectInspector: false })}>
                    <div>
                        <div className={Classes.DIALOG_BODY}>
                            <p>
                                <strong>
                                    Type: {this.state.objectDes ? this.state.objectDes.type : "?"}
                                </strong>
                            </p>
                            <p>
                                <strong>
                                    Representation:
                                </strong>
                            </p>
                            <p>
                                {this.state.objectDes ? this.state.objectDes.repr : "?"}
                            </p>

                        </div>
                        <div className={Classes.DIALOG_FOOTER}>
                            <div className={Classes.DIALOG_FOOTER_ACTIONS}>
                                <Button onClick={() => this.setState({ objectInspector: false })}>Done</Button>
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
