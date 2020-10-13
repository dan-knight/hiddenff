import React, { Component } from 'react';
import { Col, Container, Row } from 'react-bootstrap';
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
      showMenu: false,
      position: 'RB',
      data: []
    };
  };

  async componentDidMount() {
    const players = await getPlayers();
    
    this.setState(() => ({ 
      loading: false,
      data: players 
    }));
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
                data={this.state.data} />
            </Col>
          </Row>
        </Container>
      </React.Fragment>
    )
  };
};