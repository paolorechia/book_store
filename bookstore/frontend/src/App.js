import React from 'react';
import logo from './logo.svg';
import './App.css';
import Amplify from 'aws-amplify';

import { withAuthenticator } from 'aws-amplify-react'; // or 'aws-amplify-react-native';
import '@aws-amplify/ui/dist/style.css';


Amplify.configure({
  region: 'us-east-1',
  userPoolId: 'us-east-1_W9ARdc2jp',
  userPoolWebClientId: '6kr010lb4i9i3acduu3acpu28t',
})


function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default withAuthenticator(App, true);
