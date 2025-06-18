import React from "react";
import { useState } from "react";
import LoginButton from "../auth/LoginButton";
import LogoutButton from "../auth/LogoutButton";
import NavBar from "../components/NavBar";
import SaveTestDataButton from "../components/SaveReportButton";
import ReportsDisplay from "../components/ReportsDisplay";
import { useAuth0 } from "@auth0/auth0-react";
import { useNavigate } from "react-router-dom";
import "./AccountPage.css";

export default function AccountPage() {
  // Nagivation & authentication tools
  const navigate = useNavigate();
  const { isAuthenticated, user } = useAuth0();

  // State information
  const [file, setFile] = useState("");
  const [jsonData, setJsonData] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const uploadData = async () => {
    if (!file) {
      console.error("No file selected");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://127.0.0.1:5000/api/upload", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    //console.log("ReportData: ", result.reportData);

    if (result.reportData) {
      setJsonData(result.reportData);
      console.log("Report data successfully set:", result.reportData);
      navigate("/report", {
        state: { scheduleData: result.reportData },
      });

      // Remove existing data from localStorage
      localStorage.removeItem("reportData");
      localStorage.removeItem("scheduleData");
    }
  };

  // RENDERING

  if (!isAuthenticated) {
    return (
      <>
        <NavBar></NavBar>
        <div className="account-page">
          <h1>Account Page</h1>
          <p>You are not logged in. Please log in to access this page.</p>
        </div>
      </>
    );
  }

  return (
    <>
      <NavBar></NavBar>
      <div className="account-page">
        <h1>Account Page</h1>

        <div className="content">
          <div className="generate-report">
            <h2>Generate new report</h2>
            <div className="container">
              <img
                className="report-icon"
                src="/report-icon.png"
                alt="report icon"
              ></img>
              <input
                className="input-file"
                accepts=".ics"
                type="file"
                onChange={handleFileChange}
              />
              <input
                className="upload-button"
                type="submit"
                onClick={uploadData}
                value="Upload File"
              />
            </div>
          </div>
          <div className="saved-reports">
            <h2>Saved Reports</h2>
            <ReportsDisplay />
          </div>
        </div>
      </div>
    </>
  );
}

// export default AccountPage;
