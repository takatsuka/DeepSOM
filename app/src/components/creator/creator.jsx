
import * as React from 'react'
import { Component } from 'react';

import { Tag, Popover, Menu, MenuItem, Position, Button, Divider, ButtonGroup, Tab, Tabs, Intent, Spinner, Card, Elevation, Icon, Navbar, Alignment, Text, NonIdealState, Overlay } from "@blueprintjs/core";

import "./creator.scss"
import Welcome from "../welcome/welcome"
import ScatterView3D from "../scatterview_3d/scatterview"

import ProjectExplorer from '../project_explorer/project_explorer';

import SplitPane, { Pane } from 'react-split-pane';
import "../common/splitview.scss"

class Creator extends Component {
  constructor(props) {
    super(props)
    this.state = {
      tab: "sum", temp_vizData: [[1.0, 1.0, 1.0], [-1.0, -1.0, -1.0]]
    }
  }

  componentDidMount() {

  }

  onTabChange(x) {
    this.setState({ tab: x })
    if (x === "tag") this.getTags()
  }

  requestTerminate() {
    window.pywebview.api.terminate()
  }

  embedCard(whatever) {
    return (
      <Card interactive={false} elevation={Elevation.TWO}>
        {whatever}
      </Card>
    )
  }

  render() {

    var detailmap = {
      "sum": <Welcome />,
      "viz": <ScatterView3D data={this.state.temp_vizData} />
    }

    const fileMenu = (
      <Menu>
        <MenuItem icon="label" text="Open Project" />
        <MenuItem icon="graph" text="New Project" />
        <Divider />
        <MenuItem icon="graph" text="Import Data" />
      </Menu>
    )

    return (
      <>

        <Overlay isOpen={this.state.spinning_overlay} >
          <div className='loading-overlay'>
            <Card className="loading-overlay-card">
              <Spinner intent={Intent.PRIMARY} />
            </Card>
          </div>
        </Overlay>

        <Navbar className="navbar bp3-dark pywebview-drag-region">
          <Navbar.Group align={Alignment.LEFT}>
            <Navbar.Heading>PySOM Creator</Navbar.Heading>
            <Navbar.Divider />

            <Popover content={fileMenu} position={Position.BOTTOM_LEFT} placement="bottom" interactionKind="click">
              <Button className="bp3-minimal" icon="document" text="File" />
            </Popover>

            <Button className="bp3-minimal" icon="control" text="View" />
            <Button className="bp3-minimal" icon="help" text="Help" />

          </Navbar.Group>

          <Navbar.Group align={Alignment.RIGHT}>
            <Button className="bp3-minimal" icon="cross" onClick={() => this.requestTerminate()} />
          </Navbar.Group>
        </Navbar>

        <div className="detail">
          <SplitPane split="vertical" minSize={180}>

            <div className="leftpanel">
              <ProjectExplorer />

            </div>

            <div className="detail-inner">

              <div className="submenubar">
                <Tabs id="TabsExample" onChange={(x) => { this.onTabChange(x) }} selectedTabId={this.state.tab}>
                  <Tab id="sum" title="Welcome"> <Icon icon="small-cross" /> </Tab>
                  <Tab id="sch" title="SOM1 Editor"> <Icon icon="small-cross" /> </Tab>
                  <Tab id="dat" title="Data"> <Icon icon="small-cross" /> </Tab>
                  <Tab id="viz" title="Visualization"> <Icon icon="small-cross" /> </Tab>
                </Tabs>
              </div>
              <div className="submenu-spacer" />

              <div className="detail-container">
                {this.state.spinning ? <Spinner intent={Intent.PRIMARY} /> : detailmap[this.state.tab]}
              </div>

            </div>


          </SplitPane>
        </div>




      </>)

  }
}

export default Creator;
