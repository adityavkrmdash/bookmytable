// Simple feedback component used during asynchronous operations like database saving or API fetching.

const LoadingIndicator = ({ message }) => (
  <div style={{ margin: "20px", color: "#3498db", fontWeight: "bold" }}>
    {message}
  </div>
);

export default LoadingIndicator;
