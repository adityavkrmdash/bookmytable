// UI Component to display the AI Assistant's messages

const AgentBubble = ({ message }) => (
  <div className="agent-bubble">
    <p>
      <strong>Agent:</strong> {message}
    </p>
  </div>
);

export default AgentBubble;
