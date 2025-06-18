import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { useNavigate } from "react-router-dom";

const OpenReportButton = ({ report }) => {
  const { user } = useAuth0();
  const navigate = useNavigate();

  const handleOpenReport = async () => {
    if (report == null) {
      console.log("No file chosen!");
      return;
    }
    try {
    //   localStorage.setItem("reportData", report);
    //   localStorage.setItem("scheduleData", report.report.scheduleData);
      navigate("/report", {
        state: {
          scheduleData: report.report.scheduleData,
          reportData: report,
          usingSavedData: true,
        },
      });
    } catch (error) {
      console.error("Error adding saved data:", error);
    }
  };

  return <button onClick={handleOpenReport}>Open Report</button>;
};

export default OpenReportButton;
