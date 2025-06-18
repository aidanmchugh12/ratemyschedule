import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";
import AuthHandler from "./auth/AuthHandler";
import LandingPage from "./pages/LandingPage";
import AccountPage from "./pages/AccountPage";
import ReportPage from "./pages/ReportPage";
import NotFoundPage from "./pages/NotFoundPage";

import { useAuth0 } from "@auth0/auth0-react";

function App() {
  const { isLoading } = useAuth0();

  if (isLoading) {
    return <p>Loading</p>;
  }
  return (
    <Router>
      <AuthHandler />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/account" element={<AccountPage />} />
        <Route path="/report" element={<ReportPage />} />
        <Route path="/*" element={<NotFoundPage />} />
      </Routes>
    </Router>
  );
}

export default App;
