/**
 * Component to display a structured summary of the booking data before final confirmation.
 * @param {Object} data - The collected booking state from the Home component
 */
const BookingSummary = ({ data }) => {
  return (
    <table className="summary-table">
      <tbody>
        {/* Number of people for the reservation */}
        <tr>
          <td className="label">Guests</td>
          <td>{data.numberOfGuests}</td>
        </tr>
        {/* Human-readable date format (e.g., Mon Jan 26 2026) */}
        <tr>
          <td className="label">Date</td>
          <td>{data.bookingDate?.toDateString()}</td>
        </tr>
        {/* Selected time slot */}
        <tr>
          <td className="label">Time</td>
          <td>{data.bookingTime}</td>
        </tr>
        {/* Choice between Indoor or Outdoor seating */}
        <tr>
          <td className="label">Seating</td>
          <td>{data.seatingPreference}</td>
        </tr>
        {/* The user's preferred food style */}
        <tr>
          <td className="label">Cuisine</td>
          <td>{data.cuisinePreference}</td>
        </tr>
        {/* Any extra notes or dietary requirements */}
        <tr>
          <td className="label">Special Requests</td>
          <td>{data.specialRequests}</td>
        </tr>
      </tbody>
    </table>
  );
};

export default BookingSummary;
