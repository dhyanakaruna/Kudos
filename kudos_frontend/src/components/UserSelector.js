import React, { useState, useEffect } from 'react';
import apiService from '../api';

function UserSelector({ organizations, onUserSelect }) {
  const [selectedOrg, setSelectedOrg] = useState('');
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (selectedOrg) {
      loadUsers(selectedOrg);
    } else {
      setUsers([]);
    }
  }, [selectedOrg]);

  const loadUsers = async (orgId) => {
    try {
      setLoading(true);
      setError(null);
      const usersData = await apiService.getUsersByOrganization(orgId);
      setUsers(usersData);
    } catch (err) {
      setError('Failed to load users: ' + err.message);
      setUsers([]);
    } finally {
      setLoading(false);
    }
  };

  const handleUserSelect = (userId) => {
    onUserSelect(userId);
  };

  return (
    <div className="user-selector">
      <div className="org-selection">
        <label htmlFor="org-select">Select Organization:</label>
        <select 
          id="org-select"
          value={selectedOrg} 
          onChange={(e) => setSelectedOrg(e.target.value)}
        >
          <option value="">-- Choose Organization --</option>
          {organizations.map(org => (
            <option key={org.id} value={org.id}>
              {org.name}
            </option>
          ))}
        </select>
      </div>

      {selectedOrg && (
        <div className="user-selection">
          <label>Select User:</label>
          {loading && <div className="loading">Loading users...</div>}
          {error && <div className="error">{error}</div>}
          {users.length > 0 && (
            <div className="users-grid">
              {users.map(user => (
                <button
                  key={user.id}
                  className="user-card"
                  onClick={() => handleUserSelect(user.id)}
                >
                  <div className="username">{user.username}</div>
                  <div className="org-name">{user.organization_name}</div>
                </button>
              ))}
            </div>
          )}
          {!loading && users.length === 0 && selectedOrg && (
            <div className="no-users">No users found in this organization.</div>
          )}
        </div>
      )}
    </div>
  );
}

export default UserSelector;
