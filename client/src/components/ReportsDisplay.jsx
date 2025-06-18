import React, { useState, useEffect } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import OpenReportButton from "./OpenReportButton";

const ReportsDisplay = () => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { user } = useAuth0();

  const getReportsFromBackend = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/get-reports", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          sub: user.sub,
        }),
      });

      const data = await response.json();
      //console.log(data.saved_data);
      setReports(data.saved_data || []);
    } catch (error) {
      console.error("Error fetching reports:", error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user && user.sub) {
      getReportsFromBackend();
    }
  }, [user]);

  if (loading) {
    return <p>Loading reports...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  return (
    <div>
      {reports.length > 0 ? (
        <div style={{ display: "flex", flexWrap: "wrap", gap: "16px" }}>
          {reports.map((report, index) => (
            <CollapsibleReport key={index} report={report} />
          ))}
        </div>
      ) : (
        <p>No reports available.</p>
      )}
    </div>
  );
};

const CollapsibleReport = ({ report }) => {
  //console.log(report);
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        border: "1px solid #ccc",
        borderRadius: "8px",
        padding: "16px",
        backgroundColor: "#f9f9f9",
        width: "175px",
        wordWrap: "break-word",
      }}
    >
      <p>REPORT NAME</p>
      <img
        src="/saved-report-icon.png"
        alt="saved report icon"
        style={{ width: "150px", height: "auto" }}
      ></img>
      <OpenReportButton report={report}></OpenReportButton>
    </div>
  );
};

export default ReportsDisplay;
