
import * as React from 'react'
import { Component } from 'react';

import { Classes, Icon, Intent, TreeNodeInfo, Tree, Elevation, Card, Button, ButtonGroup } from "@blueprintjs/core";
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
                id: id,
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
        if(item.id.key === null) return

        window.pywebview.api.call_service(this.props.datastore, "remove_object", [item.id.key]).then((descriptor) => {
            this.refresh()
        });
    }

    handleCtxMenu(item, p, e) {
        e.preventDefault()

        PrimaryToaster.show({
            message: "Cannot add link - an identical link exists.",
            intent: Intent.WARNING,
            action: {
                text: "Yes",
                onClick: function () {
                    this.handleDelete(item)
                }.bind(this)
            }
        });

        return false
    }

    render() {

        return (
            <>
                <ButtonGroup minimal={false} elevation={Elevation.FOUR} fill={true} alignText="left" minimal={true} large={true}>
                    <Button active={true} >{this.state.workspaceName}</Button>

                </ButtonGroup>

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
