import React from 'react';

function UserInfo({ user }) {
  return (
    <div className="user-info">
      <div className="user-details">
        <h3>Welcome, {user.username}!</h3>
        <div className="user-meta">
          <div className="organization">
            <strong>Organization:</strong> {user.organization_name}
          </div>
          <div className="email">
            <strong>Email:</strong> {user.email}
          </div>
        </div>
      </div>
      
      <div className="kudos-info">
        <div className="remaining-kudos">
          <span className="kudos-count">{user.remaining_kudos}</span>
          <span className="kudos-label">
            {user.remaining_kudos === 1 ? 'kudo' : 'kudos'} remaining this week
          </span>
        </div>
        
        <div className="kudos-help">
          <small>
            You get 3 kudos every week to appreciate your colleagues!
            {user.remaining_kudos === 0 && " Kudos reset every Monday."}
          </small>
        </div>
      </div>
    </div>
  );
}

export default UserInfo;
