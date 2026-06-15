/**
 * Simple feedback component used during asynchronous operations like database saving or API fetching.
 * @param {string} message - The specific status text to display (e.g., "Confirming...")
 */
const LoadingIndicator = ({ message }) => (
  <div style={{ margin: "20px", color: "#3498db", fontWeight: "bold" }}>
    {message}
  </div>
);

export default LoadingIndicator;
