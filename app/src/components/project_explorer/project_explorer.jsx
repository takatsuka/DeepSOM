
import * as React from 'react'
import { Component } from 'react';

import { Classes, Icon, Intent, TreeNodeInfo, Tree, Elevation, Card, Button, ButtonGroup } from "@blueprintjs/core";
import { Classes as Popover2Classes, ContextMenu2, Tooltip2 } from "@blueprintjs/popover2";
import { TAG_INPUT_VALUES } from '@blueprintjs/core/lib/esm/common/classes';


class ProjectExplorer extends Component {
    constructor(props) {
        super(props)

        var treeContent = [
            {
                id: 0,
                hasCaret: true,
                isExpanded: true,
                icon: "folder-close",
                label: "Data",
                childNodes: []
            },
        ]

        this.state = {
            services: null,
            tree: treeContent,
            nInstances: 0,
        }
    }

    componentDidMount() {

    }

    addDataInstance() {
        window.pywebview.api.call_service(this.props.datastore, "open_csv_file_instance", []).then((descriptor) => {
            let newInstance = {
                id: this.state.nInstances++,
                icon: "database",
                label: descriptor,
            }
            this.state.tree[0].childNodes.push(newInstance);
            this.setState((state) => {
                return { tree: state.tree, nInstances: state.nInstances };
            });
        });
    }

    updateTree(thing){
        thing()
        this.setState({tree: this.state.tree})
    }

    render() {

        return (
            <>
                <ButtonGroup minimal={false} elevation={Elevation.FOUR} fill={true} alignText="left" minimal={true} large={true}>
                    <Button active={true} >pres-demo-2</Button>

                </ButtonGroup>

                <Tree elevation={Elevation.FOUR}
                    onNodeExpand={(x) => (this.updateTree(() => x.isExpanded = true))}
                    onNodeCollapse={(x) => (this.updateTree(() => x.isExpanded = false))}
                    contents={this.state.tree}

                />


            </>)

    }
}

export default ProjectExplorer;
