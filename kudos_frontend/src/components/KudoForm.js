import React, { useState } from 'react';
import apiService from '../api';

function KudoForm({ users, currentUser, onKudoSent }) {
  const [selectedUser, setSelectedUser] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedUser || !message.trim()) {
      setError('Please select a user and enter a message.');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setSuccess(null);

      await apiService.giveKudo(parseInt(selectedUser), message.trim());
      
      // Reset form
      setSelectedUser('');
      setMessage('');
      setSuccess('Kudo sent successfully!');
      
      // Notify parent component to refresh data
      onKudoSent();

    } catch (err) {
      setError('Failed to send kudo: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="kudo-form">
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="user-select">Give kudos to:</label>
          <select 
            id="user-select"
            value={selectedUser}
            onChange={(e) => setSelectedUser(e.target.value)}
            disabled={loading}
          >
            <option value="">-- Select a colleague --</option>
            {users.map(user => (
              <option key={user.id} value={user.id}>
                {user.username}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="message">Your message:</label>
          <textarea
            id="message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Why are you giving this kudo? Share your appreciation..."
            rows="4"
            maxLength="500"
            disabled={loading}
          />
          <small className="char-count">
            {message.length}/500 characters
          </small>
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {success && (
          <div className="success-message">
            {success}
          </div>
        )}

        <button 
          type="submit" 
          className="send-kudo-btn"
          disabled={loading || !selectedUser || !message.trim()}
        >
          {loading ? 'Sending...' : 'Send Kudo'}
        </button>
      </form>

      <div className="remaining-kudos-reminder">
        <small>
          You have <strong>{currentUser.remaining_kudos}</strong> {currentUser.remaining_kudos === 1 ? 'kudo' : 'kudos'} left this week.
        </small>
      </div>
    </div>
  );
}

export default KudoForm;
