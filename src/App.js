import React from 'react';
//import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import AboutUs from "./pages/AboutUs";
import Upload from "./pages/Upload";
import Login from "./pages/Login";
import SignUp from "./pages/SignUp";
import Profile from "./pages/Profile";
import ViewPrevious from "./pages/ViewPrevious";
import ViewResults from "./pages/viewResults";

/*function App() {
  return (
    <div className="App">
      <header className="App-header">
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
} */

export default function App() {
  return(
    <Router>
      <Switch>
        <Route path="/aboutus">
          <AboutUs />
        </Route>
        <Route path="/login">
          <Login />
        </Route>
        <Route path="/upload">
          <Upload />
        </Route>
        <Route path="/signup">
          <SignUp />
        </Route>
        <Route path="/postlogin/upload">
          <Upload />
        </Route>
        <Route path="/postlogin/profile">
          <Profile />
        </Route>
        <Route path="/postlogin/view">
          <ViewPrevious />
        </Route>
        <Route path="/postlogin/viewresults">
          <ViewResults />
        </Route>
        <Route path="/">
          <LandingPage />
        </Route>
      </Switch>
    </Router>

  );
};
