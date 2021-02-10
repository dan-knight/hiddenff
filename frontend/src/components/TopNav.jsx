import React from 'react';

export default function TopNav() {
  return (
    <nav>
      <div>
        <Links />
        <Logo />
        <Links style={{ visibility: 'hidden' }} />
      </div>
    </nav>
  );
};

const links = [
  { url: '/players', label: 'Players' },
  { url: '/teams', label: 'Teams' },
  { url: '/settings', label: 'Settings' }
];

function Links(props) {
  return (
    <ul style={props.style}>
      {links.map(l => (
        <li>
          <a href={l.url}>{l.label}</a>
        </li>
      ))}
    </ul>
  );
};

function Logo() {
  return (
    <a href="/">
      <h4 align="center"><span>hidden</span>FF</h4>
    </a>
  );
};