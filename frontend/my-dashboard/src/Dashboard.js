import React, { useEffect, useState } from "react";

export default function Dashboard() {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);    //For initial dashboard fetch
  const [scoringLoading, setScoringLoading] = useState({}); //For scoring button states
  const [error, setError] = useState(null);
  const apiBase = process.env.REACT_APP_API_BASE;

const fetchDashboardData = () => {
  fetch(`${apiBase}/dashboard_data`)
    .then(res => {
      if (!res.ok) throw new Error("Failed to fetch data");
      return res.json();
    })
    .then((data) => {
      setCandidates(data);
      setLoading(false);
      setError(null);
    })
    .catch(() => {
      setError("Failed to load candidates");
      setLoading(false);
    });
};

useEffect(() => {
  fetchDashboardData();
}, []);

  const handleScoreClick = async (interviewId) => {
  setScoringLoading(prev => ({ ...prev, [interviewId]: true }));
  try {
    const response = await fetch(
      `${apiBase}/score_interview?interview_id=${interviewId}`, 
      { method: "POST" }
    );
    if (!response.ok) throw new Error("Failed to score interview");
    const result = await response.json();

    // Optionally update candidate status in state here
    // Update candidate status to "scored"
    
    
    setCandidates(prevCandidates =>
      prevCandidates.map(candidate =>
        candidate.interview_id === interviewId
          ? { ...candidate, status: "scored" }
          : candidate
      )
    );

    // Refresh dashboard data
    fetchDashboardData();

  } catch (error) {
    alert("Error scoring interview");
  }
  setScoringLoading(prev => ({ ...prev, [interviewId]: false }));
};


  if (loading) return <p className="p-4">Processing...</p>;
  if (error) return <p className="p-4 text-red-500">{error}</p>;

  return (
  
    <div className="table-container">
  <h1>UDAO Dashboard</h1>
  <table className="dashboard-table">
    <thead>
      <tr>
        <th>Candidate</th>
        <th>Template</th>
        <th>Status</th>
        <th>Score</th>
        <th>Action</th>
      </tr>
    </thead>
    <tbody>
      {candidates.map((candidate) => (
        <tr key={candidate.candidate_id}>
          <td>{candidate.full_name}</td>
          <td>{candidate.template_name}</td>
          <td>
            {candidate.status === "scored" ? (
              <span className="text-green-600 font-medium">Scored</span>
            ) : (
              <span className="text-yellow-600 font-medium">Not Scored</span>
            )}
          </td>
          <td>{candidate.total_score !== null && candidate.total_score !== undefined ? candidate.total_score : "-"}</td> 
          <td>
            {candidate.status === "scored" ? (
              <button className="button-primary">Scored</button>
            ) : (
              <button
                disabled={!!scoringLoading[candidate.interview_id]}
                onClick={() => handleScoreClick(candidate.interview_id)}
                className={`${
                  scoringLoading[candidate.interview_id]
                    ? "button-disabled"
                    : "button-primary"
                }`}
              >
                {scoringLoading[candidate.interview_id] ? "Scoring..." : "Score"}
              </button>
            )}
          </td>
        </tr>
      ))}
    </tbody>
  </table>
</div>


  );
}
