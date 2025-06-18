import React from "react";
import NavBar from "../components/NavBar";
import { Auth0Context } from "@auth0/auth0-react";

class LandingPage extends React.Component {
  static contextType = Auth0Context;

  render() {
    const { isAuthenticated, user } = this.context;

    return (
      <>
        <NavBar></NavBar>
        <div className="landing-page">
          <h1>Welcome to the Landing Page</h1>
          <p>This is a simple landing page.</p>
          <a href="/account">To account page</a>
        </div>
      </>
    );
  }
}

export default LandingPage;
