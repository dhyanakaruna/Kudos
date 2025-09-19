import React, { useState, useEffect } from 'react';
import './App.css';
import UserSelector from './components/UserSelector';
import UserInfo from './components/UserInfo';
import KudoForm from './components/KudoForm';
import KudosList from './components/KudosList';
import apiService from './api';

function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [users, setUsers] = useState([]);
  const [organizations, setOrganizations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  // Load initial data
  useEffect(() => {
    loadInitialData();
  }, []);

  // Load current user data when user is selected
  useEffect(() => {
    if (apiService.getCurrentUserId()) {
      loadCurrentUser();
    }
  }, [refreshTrigger]);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      const orgsData = await apiService.getOrganizations();
      setOrganizations(orgsData);
      
      // If there's a stored user ID, load that user
      if (apiService.getCurrentUserId()) {
        await loadCurrentUser();
      }
    } catch (err) {
      setError('Failed to load initial data: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const loadCurrentUser = async () => {
    try {
      const userData = await apiService.getCurrentUser();
      setCurrentUser(userData);
      
      // Load users from the same organization
      const usersData = await apiService.getUsers();
      setUsers(usersData);
      
      setError(null);
    } catch (err) {
      console.error('Error loading user data:', err);
      
      // If it's an invalid user ID error, clear the stored data and show user selection
      if (err.message.includes('Invalid user ID') || err.message.includes('404')) {
        console.log('Invalid user ID detected, clearing stored user data');
        apiService.setCurrentUser(null);
        setCurrentUser(null);
        setUsers([]);
        setError(null); // Don't show error, just go back to user selection
      } else {
        setError('Failed to load user data: ' + err.message);
        setCurrentUser(null);
        setUsers([]);
        apiService.setCurrentUser(null);
      }
    }
  };

  const handleUserSelect = async (userId) => {
    try {
      apiService.setCurrentUser(userId);
      await loadCurrentUser();
    } catch (err) {
      setError('Failed to select user: ' + err.message);
    }
  };

  const handleKudoSent = () => {
    // Refresh current user data to update remaining kudos
    setRefreshTrigger(prev => prev + 1);
  };

  if (loading) {
    return (
      <div className="App">
        <div className="loading">Loading...</div>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Kudos App</h1>
        <p>Spread appreciation in your organization!</p>
      </header>

      <main className="App-main">
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {!currentUser ? (
          <div className="user-selection">
            <h2>Select Your User Account</h2>
            <UserSelector 
              organizations={organizations}
              onUserSelect={handleUserSelect}
            />
          </div>
        ) : (
          <div className="app-content">
            <div className="user-info-section">
              <UserInfo user={currentUser} />
              <button 
                className="logout-btn"
                onClick={() => {
                  apiService.setCurrentUser(null);
                  setCurrentUser(null);
                  setUsers([]);
                }}
              >
                Switch User
              </button>
            </div>

            <div className="main-sections">
              <div className="give-kudos-section">
                <h2>Give Kudos</h2>
                {currentUser.remaining_kudos > 0 ? (
                  <KudoForm 
                    users={users}
                    currentUser={currentUser}
                    onKudoSent={handleKudoSent}
                  />
                ) : (
                  <div className="no-kudos-message">
                    <p>You have no remaining kudos for this week.</p>
                    <p>Kudos reset every Monday!</p>
                  </div>
                )}
              </div>

              <div className="received-kudos-section">
                <h2>Kudos You've Received</h2>
                <KudosList userId={currentUser.id} />
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
