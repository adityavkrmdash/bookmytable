import { useEffect, useState } from "react";
import { API } from "../services/api.js";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

// Registering Chart.js components to enable Bar chart rendering
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
);

const AdminDashboard = () => {
  const [bookings, setBookings] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  /**
   * Fetches the full reservation list and the aggregated analytics data
   * Uses Promise.all to optimize API call performance
   */
  const loadDashboardData = async () => {
    setLoading(true);
    try {
      // Fetch both bookings and the analytics
      const [bookingsRes, statsRes] = await Promise.all([
        API.get("/bookings"),
        API.get("/bookings/analytics"),
      ]);
      setBookings(bookingsRes.data);
      setStats(statsRes.data);
    } catch (err) {
      console.error("Error loading dashboard data", err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Triggers a deletion request and refreshes the data view
   */
  const handleDelete = async (bookingId) => {
    if (window.confirm("Are you sure you want to cancel this booking?")) {
      try {
        await API.delete(`/bookings/${bookingId}`);
        loadDashboardData(); // Refresh both list and analytics to keep UI in sync
      } catch (err) {
        alert("Failed to delete booking.");
      }
    }
  };

  /**
   * Generates a CSV file from the current state and triggers a browser download
   */
  const exportToCSV = () => {
    const headers = [
      "Booking ID,Customer,Email,Guests,Date,Time,Seating,Cuisine,Requests\n",
    ];
    // Map booking objects into comma-separated string rows
    const rows = bookings.map(
      (b) =>
        `${b.bookingId},${b.customerName},${b.customerEmail || "N/A"},${b.numberOfGuests},${new Date(b.bookingDate).toLocaleDateString()},${b.bookingTime},${b.seatingPreference},${b.cuisinePreference},"${b.specialRequests || ""}"\n`,
    );
    // Create a Blob containing the CSV data and simulate a link click
    const blob = new Blob([headers, ...rows], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `BookMyTable_Report_${new Date().toLocaleDateString()}.csv`;
    a.click();
  };

  // Maps the backend analytics data to the format required by Chart.js
  const chartData = {
    labels: stats?.popularCuisines?.map((c) => c._id || "Other") || [],
    datasets: [
      {
        label: "Number of Bookings",
        data: stats?.popularCuisines?.map((c) => c.count) || [], // this data dtermines the height of each bar in the chart
        backgroundColor: "rgba(52, 152, 219, 0.7)",
        borderRadius: 5,
      },
    ],
  };

  if (loading) return <div className="loader">Loading Analytics...</div>;

  return (
    <div
      className="admin-container"
      style={{
        padding: "40px",
        maxWidth: "1200px",
        margin: "0 auto",
        minHeight: "100vh",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: "30px",
        }}
      >
        <h2>BookMyTable Admin Portal</h2>
        <button onClick={exportToCSV} className="btn-primary">
          📥 Download CSV Report
        </button>
      </div>

      {/* Summary Cards: Displays metrics calculated by Mongoose aggregation */}
      <div style={{ display: "flex", gap: "20px", marginBottom: "40px" }}>
        <div className="card">
          <h3>Total Bookings</h3>
          <p style={{ fontSize: "28px", color: "#2980b9" }}>
            {stats?.totalBookings || 0}
          </p>
        </div>
        <div className="card">
          <h3>Top Cuisine</h3>
          <p style={{ fontSize: "28px", color: "#27ae60" }}>
            {stats?.topCuisine || "N/A"}
          </p>
        </div>
        <div className="card">
          <h3>Busiest Time</h3>
          <p style={{ fontSize: "28px", color: "#e67e22" }}>
            {stats?.topHour || "N/A"}
          </p>
        </div>
      </div>

      {/* Chart Section: Visualizes cuisine distribution for the admin */}
      <div
        style={{
          background: "white",
          padding: "25px",
          borderRadius: "12px",
          boxShadow: "0 4px 15px rgba(0,0,0,0.05)",
          marginBottom: "40px",
        }}
      >
        <h3 style={{ marginBottom: "20px" }}>
          Cuisine Preference Distribution
        </h3>
        <div style={{ height: "300px" }}>
          <Bar
            data={chartData}
            options={{
              maintainAspectRatio: false,
              scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } },
            }}
          />
        </div>
      </div>

      {/* Detailed Table: Lists all raw booking entries */}
      <h3 style={{ marginBottom: "20px" }}>Live Reservation Log</h3>
      <div
        style={{
          overflowX: "auto",
          boxShadow: "0 4px 15px rgba(0,0,0,0.05)",
          borderRadius: "12px",
        }}
      >
        <table
          className="admin-table"
          style={{
            width: "100%",
            background: "white",
            borderCollapse: "collapse",
          }}
        >
          <thead>
            <tr
              style={{
                background: "#2c3e50",
                color: "white",
                textAlign: "left",
              }}
            >
              <th style={{ padding: "15px" }}>Customer</th>
              <th>Date</th>
              <th>Time</th>
              <th>Guests</th>
              <th>Seating</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {bookings.map((b) => (
              <tr key={b.bookingId} style={{ borderBottom: "1px solid #eee" }}>
                <td style={{ padding: "15px" }}>
                  <strong>{b.customerName}</strong>
                  <br />
                  <small style={{ color: "#7f8c8d" }}>{b.customerEmail}</small>
                </td>
                <td>{new Date(b.bookingDate).toLocaleDateString()}</td>
                <td>{b.bookingTime}</td>
                <td>{b.numberOfGuests}</td>
                <td style={{ textTransform: "capitalize" }}>
                  {b.seatingPreference}
                </td>
                <td>
                  <button
                    className="btn-cancel"
                    onClick={() => handleDelete(b.bookingId)}
                  >
                    Cancel
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <footer className="admin-footer">
        <p>
          BookMyTable Admin Portal v1.0 | Authorized Personnel Only | BUILT BY
          ADITYA VIKRAM
        </p>
      </footer>
    </div>
  );
};

export default AdminDashboard;
