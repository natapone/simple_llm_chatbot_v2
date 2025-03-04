# Pre-Sales Chatbot Data Schema

## Overview

This document defines the data schema for the pre-sales chatbot, including all Firebase Firestore collections, document structures, field types, and relationships. The schema is designed to support the conversation flow outlined in the conversation flow design document while ensuring efficient data storage and retrieval.

## Firebase Firestore Collections

The application uses the following collections in Firestore:

1. **leads**: Stores lead information collected from conversations
2. **budget_guidance**: Stores budget ranges for different project types
3. **timeline_guidance**: Stores timeline estimates for different project types
4. **conversations**: Stores conversation history for reference and analysis

## Collection Schemas

### 1. Leads Collection

**Purpose:** Store information about potential clients collected during conversations.

**Document ID:** Auto-generated

**Fields:**

| Field Name | Type | Description | Required |
|------------|------|-------------|----------|
| timestamp | Timestamp | When the lead was created | Yes |
| client_name | String | Name of the potential client | Yes |
| client_business | String | Name of the client's business | No |
| contact_information | String | Email or phone number | Yes |
| project_description | String | Brief description of the project | Yes |
| features | Array<String> | List of desired features | No |
| timeline | String | Expected timeline for the project | No |
| budget_range | String | Budget range for the project | No |
| confirmed_follow_up | Boolean | Whether the client has consented to follow-up | Yes |
| is_standard_project | Boolean | Whether the project fits standard categories | Yes |
| requires_custom_assessment | Boolean | Whether specialized assessment is needed | Yes |
| additional_notes | String | Any additional information or context | No |
| project_type | String | The type of project (website, app, etc.) | No |
| lead_source | String | How the lead was generated (default: "chatbot") | Yes |
| status | String | Current status of the lead (new, contacted, qualified, etc.) | Yes |
| assigned_to | String | ID of team member assigned to follow up | No |
| last_contact | Timestamp | When the lead was last contacted | No |

**Example Document:**
```json
{
  "timestamp": "2023-03-06T14:32:45Z",
  "client_name": "John Smith",
  "client_business": "Smith's Clothing",
  "contact_information": "john@smithsclothing.com",
  "project_description": "E-commerce website for a clothing store",
  "features": ["Product catalog", "Shopping cart", "Payment processing", "Customer accounts"],
  "timeline": "2-3 months",
  "budget_range": "$3,000-$8,000",
  "confirmed_follow_up": true,
  "is_standard_project": true,
  "requires_custom_assessment": false,
  "additional_notes": "Client is migrating from a physical store only",
  "project_type": "E-commerce site",
  "lead_source": "chatbot",
  "status": "new",
  "assigned_to": "",
  "last_contact": null
}
```

### 2. Budget Guidance Collection

**Purpose:** Store budget ranges for different project types to provide consistent guidance.

**Document ID:** Auto-generated

**Fields:**

| Field Name | Type | Description | Required |
|------------|------|-------------|----------|
| project_type | String | Type of project (e.g., "Basic website") | Yes |
| min_budget | Number | Minimum budget estimate | Yes |
| max_budget | Number | Maximum budget estimate | Yes |
| description | String | Description of what this budget covers | No |
| currency | String | Currency for the budget (default: "USD") | Yes |
| last_updated | Timestamp | When the guidance was last updated | Yes |
| factors | Array<String> | Factors that influence the budget | No |

**Example Document:**
```json
{
  "project_type": "E-commerce site",
  "min_budget": 3000,
  "max_budget": 8000,
  "description": "Online store with product listings and payment processing",
  "currency": "USD",
  "last_updated": "2023-03-01T10:15:30Z",
  "factors": ["Number of products", "Payment gateways", "Custom design", "Inventory management"]
}
```

### 3. Timeline Guidance Collection

**Purpose:** Store timeline estimates for different project types to provide consistent guidance.

**Document ID:** Auto-generated

**Fields:**

| Field Name | Type | Description | Required |
|------------|------|-------------|----------|
| project_type | String | Type of project (e.g., "Basic website") | Yes |
| min_timeline | String | Minimum timeline estimate | Yes |
| max_timeline | String | Maximum timeline estimate | Yes |
| description | String | Description of what this timeline covers | No |
| min_days | Number | Minimum number of days | Yes |
| max_days | Number | Maximum number of days | Yes |
| last_updated | Timestamp | When the guidance was last updated | Yes |
| phases | Array<Object> | Project phases and their durations | No |

**Phases Object Structure:**
```json
{
  "name": "String",
  "duration": "String",
  "description": "String"
}
```

**Example Document:**
```json
{
  "project_type": "E-commerce site",
  "min_timeline": "1 month",
  "max_timeline": "3 months",
  "description": "Online store with product listings and payment processing",
  "min_days": 30,
  "max_days": 90,
  "last_updated": "2023-03-01T10:15:30Z",
  "phases": [
    {
      "name": "Planning",
      "duration": "1-2 weeks",
      "description": "Requirements gathering and project planning"
    },
    {
      "name": "Design",
      "duration": "1-2 weeks",
      "description": "UI/UX design and approval"
    },
    {
      "name": "Development",
      "duration": "2-6 weeks",
      "description": "Frontend and backend implementation"
    },
    {
      "name": "Testing",
      "duration": "1-2 weeks",
      "description": "Quality assurance and bug fixing"
    },
    {
      "name": "Deployment",
      "duration": "1 week",
      "description": "Launch and final adjustments"
    }
  ]
}
```

### 4. Conversations Collection

**Purpose:** Store conversation history for reference, analysis, and improvement.

**Document ID:** Auto-generated session ID

**Fields:**

| Field Name | Type | Description | Required |
|------------|------|-------------|----------|
| user_id | String | Unique identifier for the user | Yes |
| session_id | String | Unique identifier for the conversation session | Yes |
| messages | Array<Object> | Array of message objects | Yes |
| created_at | Timestamp | When the conversation started | Yes |
| updated_at | Timestamp | When the conversation was last updated | Yes |
| lead_id | String | ID of the lead if one was created | No |
| conversation_summary | String | AI-generated summary of the conversation | No |
| detected_project_type | String | Project type detected during conversation | No |
| conversation_duration | Number | Duration of conversation in seconds | No |
| message_count | Number | Total number of messages in the conversation | Yes |

**Message Object Structure:**
```json
{
  "role": "String", // "system", "user", or "assistant"
  "content": "String",
  "timestamp": "Timestamp"
}
```

**Example Document:**
```json
{
  "user_id": "user_123456",
  "session_id": "session_abcdef",
  "messages": [
    {
      "role": "system",
      "content": "You are a friendly and helpful pre-sales chatbot...",
      "timestamp": "2023-03-06T14:30:00Z"
    },
    {
      "role": "user",
      "content": "Hi, I need a website for my business",
      "timestamp": "2023-03-06T14:30:15Z"
    },
    {
      "role": "assistant",
      "content": "Hello! I'd be happy to help with your website needs. What kind of business do you have?",
      "timestamp": "2023-03-06T14:30:25Z"
    }
  ],
  "created_at": "2023-03-06T14:30:00Z",
  "updated_at": "2023-03-06T14:30:25Z",
  "lead_id": "",
  "conversation_summary": "",
  "detected_project_type": "Website",
  "conversation_duration": 25,
  "message_count": 3
}
```

## Relationships Between Collections

1. **Leads ↔ Conversations**:
   - A conversation may result in a lead (one-to-one)
   - The `lead_id` field in the Conversations collection references the document ID in the Leads collection

2. **Budget Guidance ↔ Leads**:
   - Budget guidance informs lead information (many-to-many)
   - The `project_type` field in both collections creates an implicit relationship

3. **Timeline Guidance ↔ Leads**:
   - Timeline guidance informs lead information (many-to-many)
   - The `project_type` field in both collections creates an implicit relationship

## Indexes

To optimize query performance, the following indexes should be created:

1. **Leads Collection**:
   - `timestamp` (descending) for recent leads queries
   - `status`, `timestamp` (descending) for filtering leads by status
   - `assigned_to`, `status` for filtering leads by assignment

2. **Conversations Collection**:
   - `user_id`, `created_at` (descending) for user conversation history
   - `lead_id` for finding conversations related to a lead

## Data Validation Rules

### Leads Collection
- `client_name` must not be empty
- `contact_information` must contain a valid email or phone number
- `confirmed_follow_up` must be true for the lead to be stored
- `status` must be one of: "new", "contacted", "qualified", "converted", "closed"

### Budget Guidance Collection
- `min_budget` must be greater than 0
- `max_budget` must be greater than or equal to `min_budget`
- `project_type` must be unique across the collection

### Timeline Guidance Collection
- `min_days` must be greater than 0
- `max_days` must be greater than or equal to `min_days`
- `project_type` must be unique across the collection

## Data Migration and Initialization

When setting up the application for the first time, the following data should be initialized:

### Budget Guidance Initial Data
```json
[
  {
    "project_type": "Basic website",
    "min_budget": 1500,
    "max_budget": 3000,
    "description": "Simple informational website with a few pages",
    "currency": "USD",
    "last_updated": "CURRENT_TIMESTAMP",
    "factors": ["Number of pages", "Content creation", "Design complexity"]
  },
  {
    "project_type": "E-commerce site",
    "min_budget": 3000,
    "max_budget": 8000,
    "description": "Online store with product listings and payment processing",
    "currency": "USD",
    "last_updated": "CURRENT_TIMESTAMP",
    "factors": ["Number of products", "Payment gateways", "Custom design"]
  },
  {
    "project_type": "Mobile app",
    "min_budget": 5000,
    "max_budget": 15000,
    "description": "Native or cross-platform mobile application",
    "currency": "USD",
    "last_updated": "CURRENT_TIMESTAMP",
    "factors": ["Platform (iOS/Android/both)", "Complexity", "Backend integration"]
  },
  {
    "project_type": "Custom software",
    "min_budget": 10000,
    "max_budget": 50000,
    "description": "Bespoke software solution for specific business needs",
    "currency": "USD",
    "last_updated": "CURRENT_TIMESTAMP",
    "factors": ["Complexity", "Integrations", "User roles", "Data volume"]
  }
]
```

### Timeline Guidance Initial Data
```json
[
  {
    "project_type": "Basic website",
    "min_timeline": "2 weeks",
    "max_timeline": "4 weeks",
    "description": "Simple informational website with a few pages",
    "min_days": 14,
    "max_days": 28,
    "last_updated": "CURRENT_TIMESTAMP",
    "phases": [
      {
        "name": "Planning",
        "duration": "2-3 days",
        "description": "Requirements gathering and project planning"
      },
      {
        "name": "Design",
        "duration": "3-7 days",
        "description": "UI/UX design and approval"
      },
      {
        "name": "Development",
        "duration": "7-14 days",
        "description": "Implementation"
      },
      {
        "name": "Testing & Launch",
        "duration": "2-4 days",
        "description": "Quality assurance and deployment"
      }
    ]
  },
  {
    "project_type": "E-commerce site",
    "min_timeline": "1 month",
    "max_timeline": "3 months",
    "description": "Online store with product listings and payment processing",
    "min_days": 30,
    "max_days": 90,
    "last_updated": "CURRENT_TIMESTAMP",
    "phases": [
      {
        "name": "Planning",
        "duration": "1-2 weeks",
        "description": "Requirements gathering and project planning"
      },
      {
        "name": "Design",
        "duration": "1-2 weeks",
        "description": "UI/UX design and approval"
      },
      {
        "name": "Development",
        "duration": "2-6 weeks",
        "description": "Frontend and backend implementation"
      },
      {
        "name": "Testing",
        "duration": "1-2 weeks",
        "description": "Quality assurance and bug fixing"
      },
      {
        "name": "Deployment",
        "duration": "1 week",
        "description": "Launch and final adjustments"
      }
    ]
  },
  {
    "project_type": "Mobile app",
    "min_timeline": "2 months",
    "max_timeline": "4 months",
    "description": "Native or cross-platform mobile application",
    "min_days": 60,
    "max_days": 120,
    "last_updated": "CURRENT_TIMESTAMP",
    "phases": [
      {
        "name": "Planning",
        "duration": "2-3 weeks",
        "description": "Requirements gathering and project planning"
      },
      {
        "name": "Design",
        "duration": "2-3 weeks",
        "description": "UI/UX design and approval"
      },
      {
        "name": "Development",
        "duration": "4-8 weeks",
        "description": "Implementation"
      },
      {
        "name": "Testing",
        "duration": "2-4 weeks",
        "description": "Quality assurance and bug fixing"
      },
      {
        "name": "Deployment",
        "duration": "1-2 weeks",
        "description": "App store submission and launch"
      }
    ]
  },
  {
    "project_type": "Custom software",
    "min_timeline": "3 months",
    "max_timeline": "6 months",
    "description": "Bespoke software solution for specific business needs",
    "min_days": 90,
    "max_days": 180,
    "last_updated": "CURRENT_TIMESTAMP",
    "phases": [
      {
        "name": "Discovery",
        "duration": "2-4 weeks",
        "description": "In-depth requirements analysis and planning"
      },
      {
        "name": "Design",
        "duration": "2-4 weeks",
        "description": "System architecture and UI/UX design"
      },
      {
        "name": "Development",
        "duration": "8-16 weeks",
        "description": "Implementation in iterative cycles"
      },
      {
        "name": "Testing",
        "duration": "2-4 weeks",
        "description": "Quality assurance and user acceptance testing"
      },
      {
        "name": "Deployment",
        "duration": "1-2 weeks",
        "description": "System deployment and user training"
      }
    ]
  }
]
```

## Data Backup and Recovery

1. **Regular Backups**: 
   - Schedule daily backups of all collections
   - Store backups in a secure location with appropriate retention policies

2. **Point-in-Time Recovery**:
   - Enable Firestore's point-in-time recovery feature
   - Set retention period to at least 30 days

3. **Export Procedures**:
   - Implement monthly exports of lead data for integration with other systems
   - Document the process for restoring from backups

## Data Privacy and Security

1. **Personal Information**:
   - Only store personal information with explicit consent
   - Implement appropriate access controls for lead data
   - Document data retention and deletion policies

2. **Access Control**:
   - Restrict access to collections based on user roles
   - Implement field-level security where appropriate
   - Log all access to sensitive data

3. **Compliance**:
   - Ensure schema design supports GDPR compliance
   - Implement mechanisms for data subject access requests
   - Document procedures for data deletion requests

## Schema Evolution

As the application evolves, the data schema may need to be updated. Follow these guidelines for schema changes:

1. **Backward Compatibility**:
   - Ensure new schema versions are backward compatible
   - Add new fields rather than changing existing ones
   - Use default values for new required fields

2. **Migration Strategy**:
   - Document migration procedures for each schema change
   - Implement migration scripts for automated updates
   - Test migrations thoroughly before applying to production

3. **Version Tracking**:
   - Add a schema_version field to each collection
   - Update version when schema changes
   - Document each version's structure and changes

## Conclusion

This data schema provides a comprehensive foundation for the pre-sales chatbot application. It supports the conversation flow design while ensuring efficient data storage and retrieval. The schema is designed to be flexible enough to accommodate future enhancements while maintaining backward compatibility.

Regular reviews of this schema should be conducted as the application evolves to ensure it continues to meet the needs of the business and users. 