import React, { Component } from 'react';
import { Col, Container, Row } from 'react-bootstrap';

import './style/main.css';

export default class App extends Component {
  render() {
    return (
      <Container>
        <Row>
          <Col>
            <h1>Hello, world!</h1>
          </Col>
        </Row>
      </Container>
    )
  };
};