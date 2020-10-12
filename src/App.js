import React, { Component } from 'react';
import { Col, Container, Row } from 'react-bootstrap';
import Table from './components/Table';

import './style/main.css';

export default class App extends Component {
  render() {
    return (
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
    )
  };
};