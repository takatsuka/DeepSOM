
import * as React from 'react'
import { Component } from 'react';

import { Tag, Popover, Menu, MenuItem, Position, Button, ButtonGroup, Tab, Tabs, Intent, Spinner, Card, Elevation, Icon, Navbar, Alignment, Text, NonIdealState, Overlay } from "@blueprintjs/core";
import { IconNames } from "@blueprintjs/icons";
import { Column, SelectionModes, Table, Cell } from "@blueprintjs/table";

import "./creator.scss"

class Creator extends Component {
  constructor(props) {
    super(props)
    this.state = {
      tab: "sum"
    }
  }

  componentDidMount() {

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
      "sum":
        this.embedCard(<>
          <h3>Welcome to PySOM!</h3>
        </>),
    }

    const fileMenu = (
      <Menu>
        <MenuItem icon="label" text="Open Project"/>
        <MenuItem icon="graph" text="New Project"/>
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
                <Button className="bp3-minimal" icon="document" text="File"/>
            </Popover>

            <Button className="bp3-minimal" icon="graph" text="View"/>
            <Button className="bp3-minimal" icon="help" text="Help"/>

          </Navbar.Group>
        </Navbar>



        <div className="detail">

          <div className="submenubar">
            <Tabs id="TabsExample" selectedTabId={this.state.tab}>
              <Tab id="sum" title="Summary" />
              <Tab id="sch" title="Editor" />
              <Tab id="dat" title="Data"/>
              <Tab id="Visuliza" title="Visualization"/>
            </Tabs>
          </div>
          <div className="submenu-spacer" />

          <div className="detail-container">
            {this.state.spinning ? <Spinner intent={Intent.PRIMARY} /> : detailmap[this.state.tab]}
          </div>

        </div>

      </>)

  }
}

export default Creator;
