import React, { useState, useEffect } from 'react';
import apiService from '../api';

function KudosList({ userId }) {
  const [kudos, setKudos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadKudos();
  }, [userId]);

  const loadKudos = async () => {
    try {
      setLoading(true);
      setError(null);
      const kudosData = await apiService.getReceivedKudos();
      setKudos(kudosData);
    } catch (err) {
      setError('Failed to load kudos: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getTimeAgo = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);
    
    if (diffInSeconds < 60) return 'just now';
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
    if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)} days ago`;
    return formatDate(dateString);
  };

  if (loading) {
    return <div className="loading">Loading your kudos...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  if (kudos.length === 0) {
    return (
      <div className="no-kudos">
        <p>No kudos received yet!</p>
        <p>When colleagues appreciate your work, their kudos will appear here.</p>
      </div>
    );
  }

  return (
    <div className="kudos-list">
      <div className="kudos-count">
        You've received <strong>{kudos.length}</strong> {kudos.length === 1 ? 'kudo' : 'kudos'}!
      </div>
      
      <div className="kudos-items">
        {kudos.map(kudo => (
          <div key={kudo.id} className="kudo-item">
            <div className="kudo-header">
              <div className="sender-info">
                <span className="sender-name">From {kudo.sender_username}</span>
                <span className="kudo-time">{getTimeAgo(kudo.created_at)}</span>
              </div>
            </div>
            
            <div className="kudo-message">
              "{kudo.message}"
            </div>
            
            <div className="kudo-footer">
              <small className="kudo-date">
                {formatDate(kudo.created_at)}
              </small>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default KudosList;
