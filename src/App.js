import React, { Component } from 'react';
import { Col, Container, Row } from 'react-bootstrap';
import { PositionMenu } from './components/Menus';
import Table from './components/Table';
import TopNav from './components/TopNav';

import './style/main.css';

export default class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      showMenu: false,
      position: 'RB',
      data: [
        { name: 'Christian McCaffrey', position: 'RB', team: 'CAR' },
        { name: 'Dalvin Cook', position: 'RB', team: 'MIN' },
        { name: 'Alvin Kamara', position: 'RB', team: 'NO' },
        { name: 'Saquon Barkley', position: 'RB', team: 'NYG' },
        { name: 'Joe Mixon', position: 'RB', team: 'CIN' },
        { name: 'Josh Jacobs', position: 'RB', team: 'LV' },
        { name: 'Ezekiel Elliott', position: 'RB', team: 'DAL' },
        { name: 'Clyde Edwards-Elaire', position: 'RB', team: 'KC' },
        { name: 'Jonathan Taylor', position: 'RB', team: 'NO' },
        { name: 'Nick Chubb', position: 'RB', team: 'CLE' },
        { name: 'DeAndre Hopkins', position: 'WR', team: 'ARI' },
        { name: 'Michael Thomas', position: 'WR', team: 'NO' },
        { name: 'Adam Thielen', position: 'WR', team: 'MIN' },
        { name: 'Calvin Ridley', position: 'WR', team: 'ATL' },
        { name: 'Devante Adams', position: 'WR', team: 'GB' },
        { name: 'Tyreek Hill', position: 'WR', team: 'KC' },
        { name: 'Tyler Lockett', position: 'WR', team: 'SEA' },
        { name: 'D.K. Metcalf', position: 'WR', team: 'SEA' },
        { name: 'Robby Anderson', position: 'WR', team: 'CAR' },
        { name: 'Marquise Brown', position: 'WR', team: 'BAL' },
        { name: 'Tyler Boyd', position: 'WR', team: 'CIN' },
        { name: 'Odell Beckham Jr.', position: 'WR', team: 'CLE' },
        { name: 'Julian Edelman', position: 'WR', team: 'NE' },
        { name: 'Keenan Allen', position: 'WR', team: 'LAC' },
        { name: 'Terry Mclaurin', position: 'WR', team: 'WAS' },
        { name: 'Rex Burkhead', position: 'RB', team: 'NE' },
        { name: 'David Johnson', position: 'RB', team: 'HOU' },
        { name: 'Kareem Hunt', position: 'RB', team: 'CLE' },
        { name: 'Aaron Jones', position: 'RB', team: 'GB' },
        { name: 'James White', position: 'RB', team: 'NE' }
      ]
    };
  };

  toggleMenu = () => {
    this.setState(prevState => ({ showMenu: !prevState.showMenu }));
  };

  setPosition = value => {
    this.setState(() => ({ position: value }));
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
                columns={['name', 'position', 'team']} 
                data={this.state.position ? this.state.data.filter(d => d.position === this.state.position) : this.state.data} />
            </Col>
          </Row>
        </Container>
      </React.Fragment>
    )
  };
};