# Food Friend User Data Structure

## JSON Schema for User Food Preferences

Each user's data is stored in a separate JSON file: `data/users/user_[userId].json`

### Structure

```json
{
  "userId": "unique-user-id",
  "name": "User's Name",
  "foodChoices": {
    "favoriteCuisines": [
      {
        "name": "Cuisine Name",
        "rating": 1-5
      }
    ],
    "dietaryRestriction": "none|vegan|vegetarian|gluten-free|kosher|halal",
    "allergies": ["allergy1", "allergy2"],
    "spiceTolerance": 1-5,
    "likes": ["food1", "food2", "food3"],
    "dislikes": ["food1", "food2"]
  },
  "createdAt": "ISO timestamp",
  "lastUpdated": "ISO timestamp"
}
```

### Field Descriptions

- **userId**: Unique identifier for the user (UUID format)
- **name**: User's display name (username)
- **foodChoices**: Object containing all food preference data
  - **favoriteCuisines**: Array of cuisine preferences with ratings (1-5 scale)
  - **dietaryRestriction**: Primary dietary restriction (single value)
  - **allergies**: Array of food allergies
  - **spiceTolerance**: How much spice the user enjoys (1=mild, 5=very spicy)
  - **likes**: Array of specific foods/dishes the user enjoys
  - **dislikes**: Array of specific foods/dishes the user avoids
- **createdAt**: When the user profile was created
- **lastUpdated**: When the profile was last modified

### Example Files

See `data/users/user_sample.json` for a complete example.

### Usage

1. Create new user: Generate UUID, save as `user_[userId].json`
2. Update preferences: Load JSON, modify, save with new timestamp
3. Match users: Load multiple user JSONs, compare foodChoices with LLM
