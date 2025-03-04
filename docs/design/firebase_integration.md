# Firebase Integration for Lead Storage

## Overview
This document outlines how the pre-sales chatbot integrates with Firebase Firestore to store lead information collected during conversations with potential clients.

## Firebase Setup

### 1. Create a Firebase Project
1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project" and follow the setup wizard
3. Enable Google Analytics if desired (optional for MVP)

### 2. Set Up Firestore Database
1. In the Firebase Console, go to "Firestore Database"
2. Click "Create database"
3. Choose "Start in production mode" or "Start in test mode" (for MVP development)
4. Select a location for your database (choose the region closest to your users)

### 3. Create Service Account
1. In the Firebase Console, go to "Project settings" > "Service accounts"
2. Click "Generate new private key"
3. Save the JSON file securely (this contains sensitive credentials)

## Database Structure

### Collections and Documents

#### Leads Collection
The main collection for storing lead information:

```
firestore/
└── leads/
    ├── [lead_id_1]/
    │   ├── timestamp: Timestamp
    │   ├── client_name: String
    │   ├── client_business: String
    │   ├── contact_information: String
    │   ├── project_description: String
    │   ├── features: Array<String>
    │   ├── timeline: String
    │   ├── budget_range: String
    │   └── confirmed_follow_up: Boolean
    ├── [lead_id_2]/
    │   └── ...
    └── ...
```

## Integration Code

### Firebase Handler

The `firebase_handler.py` file will contain the code for interacting with Firebase:

```python
import firebase_admin
from firebase_admin import credentials, firestore
import os
import datetime

class FirebaseHandler:
    def __init__(self, credentials_path):
        """Initialize Firebase connection."""
        self.cred = credentials.Certificate(credentials_path)
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()
        
    def store_lead(self, lead_data):
        """Store lead information in Firestore.
        
        Args:
            lead_data (dict): Dictionary containing lead information
                - client_name: Name of the client
                - client_business: Client's business name
                - contact_information: Email or phone
                - project_description: Description of the project
                - features: List of desired features
                - timeline: Expected timeline
                - budget_range: Budget range
                - confirmed_follow_up: Whether follow-up is confirmed
                
        Returns:
            str: Document ID of the created lead
        """
        # Add timestamp
        lead_data['timestamp'] = datetime.datetime.now()
        
        # Store in Firestore
        lead_ref = self.db.collection('leads').document()
        lead_ref.set(lead_data)
        
        return lead_ref.id
```

## Integration with LangFlow

### 1. Custom Node in LangFlow
Create a custom node in LangFlow that:
1. Receives lead information from the conversation
2. Validates that all required fields are present
3. Calls the Firebase handler to store the lead
4. Returns a success/failure message

### 2. Decision Logic
Implement logic in the LangFlow pipeline to determine when to store lead information:
1. Check if all required fields are collected
2. Verify that the user has given consent for follow-up
3. Only then trigger the Firebase storage node

## Security Considerations

### 1. Credentials Protection
- Store Firebase credentials securely
- Use environment variables or secure storage for the credentials path
- Never commit credentials to version control

### 2. Data Validation
- Validate lead data before storing in Firebase
- Ensure all required fields are present
- Sanitize user inputs to prevent injection attacks

### 3. Access Control
- Set up Firebase Security Rules to restrict access to the leads collection
- For the MVP, only allow authenticated server access
- Consider implementing user authentication for admin access in future versions

## Example Firebase Security Rules

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Only allow authenticated server access to leads
    match /leads/{leadId} {
      allow read, write: if request.auth != null;
    }
  }
}
```

## Testing the Integration

### 1. Manual Testing
1. Run a test conversation with the chatbot
2. Provide all required information and consent for follow-up
3. Check the Firebase Console to verify the lead was stored correctly

### 2. Automated Testing
Create test cases for:
1. Successful lead storage
2. Handling missing fields
3. Error handling for Firebase connection issues

## Future Enhancements

1. **Real-time Updates**: Implement real-time listeners for new leads
2. **Lead Management**: Add functionality to update lead status (e.g., contacted, converted)
3. **Analytics**: Track conversion rates and other metrics
4. **CRM Integration**: Connect with external CRM systems
5. **Data Export**: Add functionality to export leads as CSV or other formats 