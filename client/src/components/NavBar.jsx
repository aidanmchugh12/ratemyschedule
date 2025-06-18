import { useAuth0 } from "@auth0/auth0-react";
import LoginButton from "../auth/LoginButton";
import LogoutButton from "../auth/LogoutButton";
import "./NavBar.css";

const NavBar = () => {
  const { isAuthenticated, user } = useAuth0();

  if (isAuthenticated) {
    return (
      <>
        <nav className="nav-bar">
          <div className="title-box">
            <p className="title">RateMySchedule</p>
            <a href="/">About</a>
            <a href="/account">Generate</a>
          </div>
          <div className="logged-in">
            <p>Welcome, {user.name}</p>
            <LogoutButton></LogoutButton>
          </div>
        </nav>
      </>
    );
  } else {
    return (
      <>
        <nav className="nav-bar">
          <div className="title-box">
            <p className="title">RateMySchedule</p>
            <a href="/">About</a>
            <a href="/account">Generate</a>
          </div>
          <div className="logged-out">
            <LoginButton></LoginButton>
          </div>
        </nav>
      </>
    );
  }
};

export default NavBar;
