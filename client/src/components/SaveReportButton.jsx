import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import "./SaveReportButton.css";

const SaveReportButton = ({ reportData }) => {
  const { user } = useAuth0();

  const handleSaveTestData = async () => {
    // Ensure file is chosen
    if (reportData == null) {
      console.log("No file chosen!");
      return;
    }
    //console.log(reportData);
    try {
      //console.log(user.sub);
      const response = await fetch("http://127.0.0.1:5000/api/save-report", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          sub: user.sub,
          report: reportData,
        }),
      });

      const result = await response.json();
      if (response.ok) {
        console.log(result.message);
      } else {
        console.error("Error:", result.error);
      }
    } catch (error) {
      console.error("Error adding saved data:", error);
    }
  };

  return <button onClick={handleSaveTestData}>Save Report</button>;
};

export default SaveReportButton;
