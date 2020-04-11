import React from 'react';
import logo from './logo.svg';
import './App.css';
import Amplify from 'aws-amplify';

import { withAuthenticator } from 'aws-amplify-react'; // or 'aws-amplify-react-native';
import '@aws-amplify/ui/dist/style.css';

import axios from 'axios';

const BOOKS_URL='https://devapi.paolorechia.de/books'
const API_URL='https://devapi.paolorechia.de'

Amplify.configure({
  region: 'us-east-1',
  userPoolId: 'us-east-1_W9ARdc2jp',
  userPoolWebClientId: '6kr010lb4i9i3acduu3acpu28t',
})


class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      idToken: "",
      books: []
    }
  }
  componentDidMount() {
    const idToken = (this.props.authData.signInUserSession.idToken.jwtToken);
    this.setState({"idToken": idToken}, () => console.log(this.state.idToken));
    axios.defaults.headers.common['Authorization'] = idToken;
    axios.defaults.headers.common['Content-Type'] = 'appliction/json'
    axios.get(BOOKS_URL)
      .then(res => {
        const books = res.data;
        console.log(books);
        this.setState({ books });
      })
    }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          You have the following books in DynamoDB:
          { this.state.books.map( b => (<p> {b.name} - {b.author} </p>))}

          Well done!
        </header>
      </div>
    );
  }
}

export default withAuthenticator(App, true);
