import React, { Component } from 'react';
import { Button, Col, Container, Row } from 'react-bootstrap';
import { PositionMenu } from './components/Menus';
import Table from './components/Table';
import TopNav from './components/TopNav';

import { getPlayers } from './requests';

import './style/main.css';

export default class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      loading: true,
      position: null,
      orderBy: 'last',
      showMenu: false,
      data: []
    };
  };

  componentDidMount() {
    if (this.state.loading) {
      this.updateData();
    };
  };

  componentDidUpdate() {
    if (this.state.loading) {
      this.updateData();
    };
  };

  updateData = async () => {
    const players = await this.getPlayerData();
    
    this.setState(prevState => ({ 
      loading: false,
      data: prevState.data.concat(players) 
    }));
  };

  async getPlayerData() {
    const response = await getPlayers(this.state.data.length, this.state.orderBy, this.state.position);
    return response;
  };

  loadMorePlayers = () => {
    this.setState(() => ({ loading: true }));
  };

  toggleMenu = () => {
    this.setState(prevState => ({ showMenu: !prevState.showMenu }));
  };

  setPosition = value => {
    this.setState(() => ({ 
      loading: true,
      position: value,
      data: []
    }));
  };

  setSortBy = value => {
    this.setState(() => ({
      loading: true,
      orderBy: value,
      data: []
    }));
  };

  render() {
    return (
      <React.Fragment>
        <TopNav color='light' onToggle={this.toggleMenu}/>
        <Container fluid={this.state.showMenu}>
          <Row>
            {this.state.showMenu ? <Col md={3}><PositionMenu value={this.state.position} onChange={this.setPosition} /></Col> : null}
            <Col md={this.state.showMenu ? 9 : null}>
              <Table 
                columns={[
                  { name: 'name', func: d => `${d.first} ${d.last}`, sortable: true, sortValue: 'last' },
                  { name: 'position' },
                  { name: 'team', func: d => d.team_id || '-' },
                  { name: 'total_rush_yd', label: 'Rush Yd', sortable: true},
                  { name: 'total_rec_yd', label: 'Rec Yd', sortable: true },
                  { name: 'total_pass_yd', label: 'Pass Yd', sortable: true }
                ]}
                data={this.state.data} 
                onSort={this.setSortBy}
                sortBy={this.state.orderBy} />
              <div align="center">
                <Button onClick={this.loadMorePlayers}>Show More</Button>
              </div>
            </Col>
          </Row>
        </Container>
      </React.Fragment>
    )
  };
};