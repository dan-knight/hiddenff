import React, { Component, useState } from 'react';
import { Button, Col, Container, Row } from 'react-bootstrap';
import { PositionMenu } from './components/Menus';
import PlayerTable from './components/PlayerTable';
import TopNav from './components/TopNav';

import { getPlayers } from './requests';

import './style/main.css';

export default function App() {
  const [positions, setPositions] = useState(['RB']);
  const [sortBy, setSortBy] = useState('last');
  const [showMenu, setShowMenu] = useState(false);


  function toggleMenu() {
    setShowMenu(!showMenu);
  };

  function changePositions(value) {
    setPositions(value);
  };

  function changeSortBy(value) {
    setSortBy(value);
  };

  return (
    <React.Fragment>
      <TopNav color='light' onToggle={toggleMenu}/>
      <Container fluid={showMenu}>
        <Row>
          {showMenu ? <Col md={3}><PositionMenu value={positions} onChange={changePositions} /></Col> : null}
          <Col md={showMenu ? 9 : null}>
            <PlayerTable positions={positions} sortBy={sortBy} onSort={changeSortBy} />
          </Col>
        </Row>
      </Container>
    </React.Fragment>
  );
};