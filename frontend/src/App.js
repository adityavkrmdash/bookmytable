import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  useLocation,
} from "react-router-dom";
import Home from "./pages/Home";
import AdminDashboard from "./pages/AdminDashboard";

/**
 * Navigation Component
 */
const Navigation = () => {
  const location = useLocation();

  return (
    <nav className="nav-bar" style={{ padding: "10px", background: "#2c3e50" }}>
      <Link
        className={`nav-link ${location.pathname === "/" ? " active" : ""}`}
        to="/"
      >
        Booking
      </Link>
      <Link
        className={`nav-link ${location.pathname === "/admin" ? " active" : ""}`}
        to="/admin"
      >
        Admin Panel
      </Link>
    </nav>
  );
};

/**
 * Main Entry Point Component
 * Manages global routing and navigation
 */

function App() {
  return (
    <Router>
      <Navigation />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/admin" element={<AdminDashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
