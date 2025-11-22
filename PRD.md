# Product Requirements Document: Food-Friend

## 1. Executive Summary

**Product Name:** Food-Friend  
**Version:** 1.0 (Hackathon MVP)  
**Date:** November 22, 2025  
**Document Owner:** Product Team  
**Status:** Draft  
**Timeline:** 1 hour hackathon project

### 1.1 Product Overview
Food-Friend is a social food preference matching application that helps groups of people discover their best matches based on food preferences and dietary choices. Using local AI-powered matching algorithms via llama.cpp, the platform analyzes user food preferences to suggest compatible friends for dining experiences, meal sharing, and food-related social activities.

### 1.2 Business Objectives
- Connect people with similar food preferences and dietary habits
- Facilitate social dining experiences through intelligent matching
- Build a community around shared food interests
- Provide privacy-focused, local AI matching without cloud dependencies
- Enable seamless group dining decisions

## 2. Product Vision & Goals

### 2.1 Vision Statement
To create meaningful social connections through shared food preferences, making it easier for people to find dining companions, plan group meals, and discover friends with compatible tastes - all powered by privacy-focused local AI.

### 2.2 Success Metrics
- User engagement: 3+ sessions per week
- Match accuracy: 80%+ user satisfaction with friend matches
- User retention: 60% after 3 months
- Social connections: Average 5+ matches per user
- Group formation: 40% of users join or create dining groups
- User satisfaction: NPS score of 50+

## 3. Target Audience

### 3.1 Primary Users
- **Young Professionals & Students** (18-35 years old)
  - Need: Find friends with similar food preferences in new cities
  - Pain points: Difficulty finding compatible dining companions, dietary restrictions isolation
  
- **Food Enthusiasts** (25-45 years old)
  - Need: Connect with like-minded foodies for restaurant exploration
  - Pain points: Friends with different tastes, lack of adventurous dining partners

- **People with Dietary Restrictions** (All ages)
  - Need: Find others with similar dietary needs (vegan, gluten-free, halal, kosher, etc.)
  - Pain points: Feeling excluded from social dining, limited compatible social circles

### 3.2 Secondary Users
- Remote workers seeking local social connections
- Expats and travelers looking for food culture connections
- Cooking enthusiasts wanting to share meals
- Event organizers planning group dining experiences

## 4. Core Features & Requirements

### 4.1 User Profile & Food Preferences
**Priority:** P0 (Must Have)

**Description:** Allow users to create profiles and specify detailed food preferences.

**Requirements:**
- **Simple username-only login** (no password for hackathon speed)
- Profile creation with minimal info (username, optional bio)
- Streamlined food preference selection:
  - Top 3-5 favorite cuisines (Italian, Japanese, Mexican, Indian, etc.)
  - Primary dietary restriction (if any): vegan, vegetarian, gluten-free, etc.
  - Major allergies (if any)
  - Spice tolerance level (1-5 scale)
  - Quick likes/dislikes (free text or tags)
- Simple preference weighting

**Acceptance Criteria:**
- Profile setup completed in under 2 minutes
- Minimum 10 preference categories available
- Data saved to individual JSON file per user
- Preferences editable at any time
- Changes reflected immediately in matching algorithm

### 4.2 JSON-based Data Storage
**Priority:** P0 (Must Have)

**Description:** Store user data in individual JSON text files for simplicity and portability.

**Requirements:**
- One JSON file per user (e.g., `user_[id].json`)
- Structured data format including:
  - User profile information
  - Food preferences with weights
  - Match history
  - Timestamps for updates
- File-based CRUD operations (Create, Read, Update, Delete)
- Data validation and error handling
- Backup mechanism for data integrity
- File locking to prevent concurrent write conflicts

**Acceptance Criteria:**
- JSON files human-readable and well-formatted
- Read/write operations complete in <100ms
- Data persistence across application restarts
- Corrupted file detection and recovery
- Maximum file size monitoring

### 4.3 AI-Powered Friend Matching
**Priority:** P0 (Must Have)

**Description:** Use llama.cpp with a local LLM to calculate compatibility scores and suggest friend matches.

**Requirements:**
- Integration with llama.cpp for local LLM inference
- Compatibility algorithm using LLM to:
  - Analyze food preference similarities
  - Weight preferences by importance
  - Generate compatibility scores (0-100)
  - Provide reasoning for matches
- Match suggestion interface showing:
  - User profiles of matches
  - Compatibility percentage
  - Shared preferences highlighted
  - Difference areas noted
- Filtering options (dietary restrictions, location, etc.)
- Configurable match radius/criteria
- Batch processing for efficient matching
- Match refresh/update mechanism

**Acceptance Criteria:**
- LLM loads successfully on application start
- Matching calculation completes in <5 seconds for 100 users
- Score accuracy validated through user feedback
- Clear explanation of why users matched
- Minimum 70% user satisfaction with match quality
- Local processing without external API calls

### 4.4 Match Browsing & Discovery
**Priority:** P0 (Must Have)

**Description:** Interface for users to browse and interact with their matches.

**Requirements:**
- Match feed showing top compatible users
- Sortable by compatibility score, recent activity
- User profile view with detailed preferences
- "Like" or "Connect" functionality
- Match filtering (dietary restrictions)
- Search functionality for specific preferences

**Acceptance Criteria:**
- Display top 3 matches on initial load
- Smooth scrolling and pagination
- Profile loads in <1 second
- Real-time updates when preferences change

### 4.5 Connection Management
**Priority:** P1 (Should Have)

**Description:** Manage connections between matched users.

**Requirements:**
- Send connection requests
- Accept/decline requests
- Friends list
- Connection status indicators
- Messaging or chat capability (basic)
- Remove connections
- Connection activity notifications

**Acceptance Criteria:**
- Connection request sent/received in <2 seconds
- Notifications delivered in real-time
- Friends list accessible offline

### 4.6 Group Formation
**Priority:** P1 (Should Have)

**Description:** Enable users to form groups based on compatible food preferences.

**Requirements:**
- Create dining groups
- Invite connections to groups
- Group compatibility score calculation
- Group chat/discussion
- Event planning (restaurant choice, time, location)
- Group preference aggregation
- Leave/dissolve group functionality

**Acceptance Criteria:**
- Group created in under 1 minute
- Group compatibility score calculated for 2-10 members
- Invitations sent instantly
- Group recommendations based on collective preferences

### 4.7 Preference Analytics
**Priority:** P2 (Nice to Have)

**Description:** Provide insights into user's food preferences and match patterns.

**Requirements:**
- Personal taste profile visualization
- Match statistics and trends
- Most compatible cuisines/preferences
- Preference evolution over time
- Comparison with community trends
- Recommendation insights from LLM

**Acceptance Criteria:**
- Analytics generated in <3 seconds
- Visual charts clear and informative
- Privacy-preserving aggregate statistics

## 5. User Experience Requirements

### 5.1 Mobile Experience
- Responsive design for phones and tablets
- Native apps for iOS and Android
- Touch-optimized interface
- Camera integration for barcode scanning
- Push notifications
- Offline functionality for core features

### 5.2 Web Experience
- Responsive web application
- Modern browser support (Chrome, Firefox, Safari, Edge)
- Desktop-optimized layouts
- Keyboard shortcuts for power users

### 5.3 Accessibility
- WCAG 2.1 AA compliance
- Screen reader support
- High contrast mode
- Font size adjustments
- Keyboard navigation

## 6. Technical Requirements

### 6.1 Performance
- Application launch time: <3 seconds
- LLM model loading: <10 seconds on first launch
- Match calculation: <5 seconds for 100 user comparisons
- JSON file read/write: <100ms per operation
- UI responsiveness: 60fps for smooth interactions
- 99.9% uptime for core features

### 6.2 LLM Integration (llama.cpp)
- Local LLM inference using llama.cpp
- Model selection: Compatible GGUF models (7B-13B parameters recommended)
- Model storage and versioning
- Efficient prompt engineering for preference matching
- Context window management
- Inference optimization (GPU acceleration if available)
- Fallback mechanisms if LLM unavailable
- Model update capability

### 6.3 Data Storage
- JSON text files for user data storage
- File naming convention: `user_[uuid].json`
- Directory structure for organization
- File locking for concurrent access prevention
- Automatic backup system (daily)
- Data validation on read/write
- Corruption detection and recovery
- Maximum file size limits (1MB per user recommended)

### 6.4 Security
- **Username-only authentication** (no passwords for hackathon)
- Simple session management (username stored in session)
- Basic file permission controls
- Input validation and sanitization
- Basic XSS prevention
- **Note:** Production would require proper authentication

### 6.5 Privacy
- Local-only AI processing (no cloud dependencies)
- User data stays on local/server storage
- GDPR and CCPA compliance
- User data export functionality
- Right to be forgotten implementation
- Transparent data usage policies
- Optional profile visibility controls

### 6.6 Scalability
- Support 10,000+ users initially
- Efficient file indexing for quick lookups
- Batch processing for match calculations
- Caching layer for frequently accessed data
- Database migration path if needed later
- Horizontal scaling considerations

### 6.7 Technology Stack Recommendations
- **Backend:** Python/Node.js/Go
- **LLM:** llama.cpp with GGUF models
- **Frontend:** React/Vue.js/Svelte
- **Authentication:** JWT tokens
- **File Management:** Native filesystem APIs
- **Optional Cache:** Redis for match results
- **Optional Search:** Elasticsearch for user discovery

## 7. Data Requirements

### 7.1 User Data Model (JSON Structure)
```json
{
  "userId": "uuid-string",
  "profile": {
    "username": "string",
    "email": "string",
    "displayName": "string",
    "bio": "string",
    "location": {
      "city": "string",
      "country": "string",
      "coordinates": {"lat": 0.0, "lng": 0.0}
    },
    "profilePhoto": "url-string",
    "createdAt": "timestamp",
    "lastUpdated": "timestamp"
  },
  "foodPreferences": {
    "cuisines": [
      {"name": "Italian", "preference": 5, "importance": 4},
      {"name": "Japanese", "preference": 4, "importance": 3}
    ],
    "dietaryRestrictions": ["vegan", "gluten-free"],
    "allergies": ["peanuts", "shellfish"],
    "spiceLevel": 3,
    "mealTypes": ["lunch", "dinner", "desserts"],
    "priceRange": {"min": 2, "max": 4},
    "diningPreferences": ["restaurant", "homeCooking", "streetFood"],
    "specificLikes": ["pasta", "sushi", "tacos"],
    "specificDislikes": ["liver", "oysters"],
    "adventurousness": 4
  },
  "matchHistory": [
    {
      "matchedUserId": "uuid-string",
      "compatibilityScore": 85,
      "matchedAt": "timestamp",
      "status": "connected"
    }
  ],
  "connections": ["uuid-1", "uuid-2"],
  "groups": ["group-uuid-1"],
  "settings": {
    "visibility": "public",
    "matchRadius": 50,
    "notifications": true
  }
}
```

### 7.2 Data Storage Structure
```
data/
├── users/
│   ├── user_[uuid-1].json
│   ├── user_[uuid-2].json
│   └── ...
├── groups/
│   ├── group_[uuid-1].json
│   └── ...
├── backups/
│   └── [date]/
│       └── users/
└── models/
    └── llama-model.gguf
```

### 7.3 Data Operations
- **Create:** New user registration creates JSON file
- **Read:** Load user data on login or match calculation
- **Update:** Preference changes update JSON file with timestamp
- **Delete:** User deletion removes JSON file and references

### 7.4 Data Retention
- Active user data: Indefinite while account active
- Deleted user data: 30 days grace period, then permanent deletion
- Backups: Daily for 7 days, weekly for 4 weeks, monthly for 6 months
- Match history: Last 100 matches per user
- Analytics: Anonymous aggregate data for 1 year

## 8. Design Requirements

### 8.1 Visual Design
- Modern, friendly, and approachable aesthetic
- Food-centric color palette (warm oranges, appetizing reds, fresh greens)
- High-quality food imagery and icons
- Clean card-based layouts for user profiles
- Percentage indicators for compatibility scores
- Visual preference comparison charts
- Responsive design for all screen sizes

### 8.2 User Experience
- Intuitive preference selection with sliders and multi-select
- Swipe-based or card-based match browsing
- Clear visual indicators for match quality
- Easy-to-understand compatibility explanations
- Smooth transitions and micro-interactions
- Minimal clicks to complete key actions
- Onboarding flow for first-time users

### 8.3 Branding
- Logo emphasizing connection and food
- Tone of voice: Friendly, inclusive, food-enthusiastic
- Tagline examples: "Find Your Foodie Match", "Connect Through Taste"
- Community-focused messaging

## 9. Constraints & Assumptions

### 9.1 Constraints
- **Timeline: 1 hour hackathon project**
- **Scope: Core matching functionality only**
- Local LLM processing requires sufficient hardware (minimum 8GB RAM recommended)
- File-based storage (perfect for hackathon demo)
- LLM inference speed depends on hardware capabilities
- No password authentication (username only for speed)

### 9.2 Assumptions
- Users have devices capable of running the application
- Local LLM processing acceptable for initial MVP
- Users willing to share detailed food preferences
- File-based JSON storage sufficient for MVP user base (<1,000 users)
- Users interested in social connections based on food
- Privacy-focused local AI is a selling point
- Match algorithm accuracy improves with user feedback

## 10. Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Low user adoption | High | Medium | Strong marketing, referral program, freemium model |
| Inaccurate nutritional data | High | Low | Partner with verified databases, allow user corrections |
| Recipe licensing issues | Medium | Medium | Partner with content creators, user-generated content |
| Barcode database limitations | Medium | Medium | Multiple database integrations, manual entry fallback |
| Competition from established apps | High | High | Unique features, better UX, community building |
| Privacy concerns | High | Low | Transparent policies, minimal data collection, encryption |

## 11. Release Strategy

### 11.1 Hackathon MVP (1 Hour)
**Core Demo Features:**
- Simple username login (no password)
- Quick preference input form (5-7 key preferences)
- JSON file storage per user
- LLM-based matching for 2-5 demo users
- Basic match display with compatibility scores
- Minimal UI (can be CLI or simple web interface)

**Success Criteria:**
- Working demo showing preference input
- LLM calculates match scores
- Display top matches with explanations
- Data persists in JSON files

### 11.2 Post-Hackathon Enhancements (If Continued)
- Proper authentication
- Enhanced UI/UX
- Connection management
- Group formation
- Mobile app
- Scalability improvements

## 12. Success Criteria

### 12.1 Hackathon Demo Success Criteria
- Username-based login working
- Preference form functional
- JSON files created and readable
- LLM integration working (llama.cpp)
- Match scores calculated and displayed
- Demo works for 3-5 test users
- Clear explanation of matching logic
- Presentable in 3-5 minute demo

### 12.2 Minimum Viable Demo
- 1 user can create profile with username
- 1 user can add food preferences
- System saves to JSON file
- LLM calculates compatibility with other users
- Results displayed with scores

## 13. Hackathon Technical Decisions

1. **LLM Model:** Which lightweight GGUF model? (Recommend: Llama 3.2 3B or Phi-3)
2. **Interface:** CLI, basic web app, or simple GUI?
3. **Language:** Python (fastest), Node.js, or Go?
4. **Matching Algorithm:** Simple prompt-based or more sophisticated?
5. **Number of Preferences:** 5-7 key preferences or more?
6. **Demo Data:** Pre-populate sample users or live entry only?
7. **UI Framework:** Plain HTML/CSS, or quick framework (Flask, Express)?

## 14. Implementation Priority Order (1 Hour)

**Minutes 0-10:** Setup & Structure
- Initialize project structure
- Set up llama.cpp integration
- Create data directory for JSON files

**Minutes 10-20:** User & Preference System
- Username-only login
- Simple preference input (form or CLI)
- JSON save functionality

**Minutes 20-40:** LLM Matching
- LLM prompt engineering for compatibility
- Calculate scores for user pairs
- Generate match explanations

**Minutes 40-50:** Display & Results
- Show match results interface
- Display compatibility scores
- Show shared preferences

**Minutes 50-60:** Testing & Polish
- Test with 3-5 sample users
- Fix critical bugs
- Prepare demo presentation

## 14. Appendices

### 14.1 Competitive Analysis
(To be completed: Analysis of MyFitnessPal, Yummly, Paprika, Too Good To Go, etc.)

### 14.2 User Research
(To be completed: Survey results, user interviews, persona development)

### 14.3 Wireframes & Mockups
(To be attached: UI/UX designs for key screens)

### 14.4 Technical Architecture
(To be completed: System architecture diagrams, tech stack decisions)

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-22 | Product Team | Initial draft |

## Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Manager | | | |
| Engineering Lead | | | |
| Design Lead | | | |
| Business Owner | | | |
