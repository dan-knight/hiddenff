import React, { Component } from 'react';
import { Col, Container, Row } from 'react-bootstrap';
import Table from './components/Table';
import TopNav from './components/TopNav';

import './style/main.css';

export default class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      showMenu: false
    };
  };

  toggleMenu = () => {
    this.setState(prevState => ({ showMenu: !prevState.showMenu }));
  };

  render() {
    return (
      <React.Fragment>
        <TopNav color='light' onToggle={this.toggleMenu}/>
        <Container>
          <Row>
            <Col>
              <Table 
                columns={['name', 'position', 'team']} 
                data={[
                  { name: 'Christian McCaffrey', position: 'RB', team: 'CAR' },
                  { name: 'Dalvin Cook', position: 'RB', team: 'MIN' },
                  { name: 'Alvin Kamara', position: 'RB', team: 'NO' }
                ]} />
            </Col>
          </Row>
        </Container>
      </React.Fragment>
    )
  };
};