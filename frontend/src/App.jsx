import { useState } from 'react'
import './App.css'

const API_URL = 'http://localhost:5000/api'

function App() {
  const [userName, setUserName] = useState('')
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [foodInput, setFoodInput] = useState('')
  const [foodChoices, setFoodChoices] = useState([])
  const [matches, setMatches] = useState([])
  const [isCalculating, setIsCalculating] = useState(false)
  const [error, setError] = useState('')

  const handleLogin = async (e) => {
    e.preventDefault()
    if (!userName.trim()) return

    try {
      const response = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: userName.trim() })
      })

      const data = await response.json()
      
      if (data.success) {
        setIsLoggedIn(true)
        setFoodChoices(data.user.foodChoices || [])
        setError('')
      } else {
        setError(data.error || 'Login failed')
      }
    } catch (err) {
      setError('Failed to connect to server. Make sure the backend is running.')
      console.error(err)
    }
  }

  const handleAddFood = async (e) => {
    e.preventDefault()
    if (!foodInput.trim()) return

    const newChoices = [...foodChoices, foodInput.trim()]
    setFoodChoices(newChoices)
    setFoodInput('')

    // Update on backend
    try {
      await fetch(`${API_URL}/update-foods`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          name: userName,
          foodChoices: newChoices 
        })
      })
    } catch (err) {
      console.error('Failed to update foods:', err)
    }
  }

  const handleRemoveFood = async (index) => {
    const newChoices = foodChoices.filter((_, i) => i !== index)
    setFoodChoices(newChoices)

    // Update on backend
    try {
      await fetch(`${API_URL}/update-foods`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          name: userName,
          foodChoices: newChoices 
        })
      })
    } catch (err) {
      console.error('Failed to update foods:', err)
    }
  }

  const handleCalculateMatches = async () => {
    if (foodChoices.length === 0) {
      setError('Please add some food preferences first')
      return
    }

    setIsCalculating(true)
    setError('')

    try {
      const response = await fetch(`${API_URL}/calculate-matches`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: userName })
      })

      const data = await response.json()
      
      if (data.success) {
        setMatches(data.matches)
      } else {
        setError(data.error || 'Failed to calculate matches')
        setMatches([])
      }
    } catch (err) {
      setError('Failed to calculate matches. Make sure the backend is running.')
      console.error(err)
      setMatches([])
    } finally {
      setIsCalculating(false)
    }
  }

  const handleLogout = () => {
    setIsLoggedIn(false)
    setUserName('')
    setFoodChoices([])
    setMatches([])
    setError('')
  }

  if (!isLoggedIn) {
    return (
      <div className="app centered">
        <div className="login-container">
          <h1>🍕 Food-Friend</h1>
          <p>Find your foodie matches!</p>
          {error && <div className="error-message">{error}</div>}
          <form onSubmit={handleLogin}>
            <input
              type="text"
              placeholder="Enter your name"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              className="input-field"
            />
            <button type="submit" className="btn-primary">
              Enter
            </button>
          </form>
        </div>
      </div>
    )
  }

  return (
    <div className="app">
      <header>
        <h1>🍕 Food-Friend</h1>
        <p>Welcome, {userName}!</p>
        <button onClick={handleLogout} className="btn-logout">
          Switch User
        </button>
      </header>

      {error && <div className="error-banner">{error}</div>}

      <div className="main-content">
        <div className="food-section">
          <h2>Your Food Preferences</h2>
          <form onSubmit={handleAddFood} className="food-form">
            <input
              type="text"
              placeholder="Enter a food you like..."
              value={foodInput}
              onChange={(e) => setFoodInput(e.target.value)}
              className="input-field"
            />
            <button type="submit" className="btn-secondary">
              Add Food
            </button>
          </form>

          <div className="food-list">
            {foodChoices.length === 0 ? (
              <p className="empty-state">No food preferences yet. Add some!</p>
            ) : (
              foodChoices.map((food, index) => (
                <div key={index} className="food-tag">
                  {food}
                  <button 
                    onClick={() => handleRemoveFood(index)}
                    className="remove-btn"
                  >
                    ×
                  </button>
                </div>
              ))
            )}
          </div>

          <button 
            onClick={handleCalculateMatches}
            disabled={foodChoices.length === 0 || isCalculating}
            className="btn-primary btn-large"
          >
            {isCalculating ? 'Calculating with LLM...' : '🔍 Calculate Matches'}
          </button>
        </div>

        <div className="matches-section">
          <h2>Your Matches</h2>
          {matches.length === 0 ? (
            <p className="empty-state">
              {isCalculating ? 'Finding your matches using AI...' : 'Add food preferences and click "Calculate Matches"'}
            </p>
          ) : (
            <div className="matches-list">
              {matches.map((match, index) => (
                <div key={index} className="match-card">
                  <div className="match-header">
                    <h3>{match.name}</h3>
                    <div className="match-score">
                      {match.score}%
                    </div>
                  </div>
                  {match.sharedFoods && match.sharedFoods.length > 0 && (
                    <div className="shared-foods">
                      <strong>Shared dishes:</strong> {match.sharedFoods.join(', ')}
                    </div>
                  )}
                  {match.matchedCuisines && match.matchedCuisines.length > 0 && (
                    <div className="shared-foods">
                      <strong>Matched cuisines:</strong> {match.matchedCuisines.join(', ')}
                    </div>
                  )}
                  {match.keywordHits && match.keywordHits.length > 0 && (
                    <div className="shared-foods">
                      <strong>Similar tastes:</strong> {match.keywordHits.join(', ')}
                    </div>
                  )}
                  {match.llmReason && (
                    <div className="llm-reason">
                      <strong>AI Analysis:</strong> {match.llmReason}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
