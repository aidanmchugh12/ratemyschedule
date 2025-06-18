import React, { useEffect, useState } from "react";
import LoginButton from "../auth/LoginButton";
import { useAuth0 } from "@auth0/auth0-react";
import { useLocation, useNavigate } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import "./ReportPage.css";
import SaveReportButton from "../components/SaveReportButton";

export default function ReportPage() {
  // Nagivation & authentication tools
  const navigate = useNavigate();
  const { isAuthenticated, user } = useAuth0();
  const location = useLocation();

  // State Information
  const [scheduleData, setScheduleData] = useState(
    location.state?.scheduleData
  );
  const [reportData, setReportData] = useState(location.state?.reportData);
  const [usingSavedData, setUsingSavedData] = useState(
    location.state?.usingSavedData || false
  );
  const [loading, setLoading] = useState(false);

  // Only fetch if we have scheduleData but no reportData
  useEffect(() => {
    if (!reportData && scheduleData) {
      setLoading(true);
      fetch("http://127.0.0.1:5000/api/generate-new-report", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ scheduleData }),
      })
        .then((res) => res.json())
        .then((data) => {
          setReportData(data);
          // localStorage.setItem("reportData", JSON.stringify(data));
          // localStorage.setItem("scheduleData", JSON.stringify(scheduleData));
          setLoading(false);
        })
        .catch(() => setLoading(false));
    }
  }, [scheduleData, reportData]);

  if (!isAuthenticated) {
    return (
      <div className="report-page">
        <h1>Report Page</h1>
        <p>You are not logged in. Please log in to access this page.</p>
        <LoginButton />
      </div>
    );
  }

  if (!scheduleData) {
    return (
      <div className="report-page">
        <h1>Report Page</h1>
        <p>You have not generated a report. Head back to account page!</p>
      </div>
    );
  }

  if (loading || !reportData) {
    return (
      <div className="report-page">
        <h1>Generating Report...</h1>
        <p>Please wait!</p>
      </div>
    );
  }

  return (
    <>
      <div className="report-page">
        <h1>Your Schedule Report</h1>
        <div className="score-card">
          <div className="overall">
            <div className="title">Overall Score: </div>
            <div className="score">
              {reportData?.report?.reportData?.scores?.overallScore}
            </div>
          </div>
          <div className="individual">
            <div className="sub-score">
              <div className="sub-title">Instructor Score: </div>
              <div className="individual-score">
                {reportData?.report?.reportData?.scores?.instructorEvalScore}
              </div>
            </div>
            <div className="sub-score">
              <div className="sub-title">Break Score: </div>
              <div className="individual-score">
                {reportData?.report?.reportData?.scores?.timeMetricsScore}
              </div>
            </div>
            <div className="sub-score">
              <div className="sub-title">Credit Score: </div>
              <div className="individual-score">
                {reportData?.report?.reportData?.scores?.academicRigorScore}
              </div>
            </div>
          </div>
        </div>

        <h2>Instructor Analysis</h2>
        <h3>
          Score: {reportData?.report?.reportData?.scores?.instructorEvalScore}
          /100
        </h3>
        <div className="instructor-report">
          <div className="instructor-summary">
            {reportData?.report?.reportData?.instructorEval?.summary}
          </div>
          <div className="instructor-card">
            <div className="card-title">Instructor RateMyProfessor Links</div>
            <div className="instructor-segments">
              {reportData?.report?.reportData?.instructorEval
                ?.instructorLinks &&
                Object.entries(
                  reportData.report.reportData.instructorEval.instructorLinks
                ).map(([name, link], idx) => (
                  <div key={idx} className="instructor-segment">
                    <div className="class-name">
                      {
                        reportData?.report?.reportData?.instructorEval
                          ?.instructorClasses[name]
                      }
                    </div>
                    <span className="dot-leader"></span>
                    <a
                      className="instructor-link"
                      href={link}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      {name}
                    </a>
                  </div>
                ))}
            </div>
          </div>
        </div>
        <h2>Breaks Analysis</h2>
        <h3>
          Score: {reportData?.report?.reportData?.scores?.timeMetricsScore}/100
        </h3>
        <div className="breaks-report">
          <ReactMarkdown>
            {reportData?.report?.reportData?.timeMetrics?.summary}
          </ReactMarkdown>
        </div>
        <h2>Credits Analysis</h2>
        <h3>
          Score: {reportData?.report?.reportData?.scores?.academicRigorScore}
          /100
        </h3>
        <div className="credits-report">
          <ReactMarkdown>
            {reportData?.report?.reportData?.academicRigor?.summary}
          </ReactMarkdown>
        </div>
        {usingSavedData ? (
          ""
        ) : (
          <SaveReportButton reportData={reportData}></SaveReportButton>
        )}
        {/* <h2>Schedule Data</h2>
        <pre>{JSON.stringify(JSON.parse(scheduleData), null, 2)}</pre> */}
        {/* <h2>Report Data</h2> */}
        <pre>{JSON.stringify(reportData, null, 2)}</pre>
      </div>
    </>
  );
}
