// src/api.js
export async function fetchDashboardData() {
  try {
    const response = await fetch("/dashboard_data"); // proxy will forward this
    if (!response.ok) {
      throw new Error("Network response was not ok " + response.statusText);
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching dashboard data:", error);
    return null;
  }
}
