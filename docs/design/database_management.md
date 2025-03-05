# Database Management

## Overview

This document outlines the database management approach for the Simple LLM Chatbot v2 project. The project uses TinyDB for local data storage, with a focus on maintainability and version control compatibility.

## Database Structure

The database is a JSON file managed by TinyDB, containing the following tables:

- `budget_guidance`: Contains budget guidance information for different project types
- `timeline_guidance`: Contains timeline guidance information for different project types
- `leads`: Stores lead information collected from user interactions
- `conversations`: Stores conversation history between users and the chatbot

## Seed Data

To ensure consistent initial data and to facilitate version control, the project uses a seed data approach:

1. Initial data is stored in `data/seed_data.json`
2. This file contains only reference data (budget and timeline guidance)
3. The seed data file is included in version control
4. User-generated data (leads, conversations) is not included in the seed data

## Database Initialization

The database is initialized using the `app/db_init.py` script, which:

1. Reads the seed data from `data/seed_data.json`
2. Creates the database file at the location specified by the `TINYDB_PATH` environment variable
3. Initializes the `DatabaseHandler` with `initialize_default_data=False` to prevent duplicate data
4. Populates the database with the seed data
5. Logs the initialization process

To initialize or reset the database:

```bash
python app/db_init.py
```

## DatabaseHandler Class

The `DatabaseHandler` class provides an interface to TinyDB and includes the following features:

1. **Initialization Options**:
   - `db_path`: Path to the TinyDB JSON file
   - `initialize_default_data`: Boolean flag to control whether default data should be initialized (default: `True`)

2. **Default Data Initialization**:
   - When `initialize_default_data` is `True`, the handler will initialize default data if tables are empty
   - When `initialize_default_data` is `False`, the handler will not initialize default data, allowing for manual data population

3. **Table Management**:
   - Creates and manages tables for `leads`, `budget_guidance`, and `timeline_guidance`
   - Provides methods for CRUD operations on these tables

## Version Control

To prevent conflicts and unnecessary commits, the database file is excluded from version control:

1. The `.gitignore` file includes patterns to exclude database files:
   ```
   data/chatbot_db.json
   data/chatbot_db.json.*
   ```

2. The seed data file is explicitly included:
   ```
   !data/seed_data.json
   ```

This approach ensures that:
- Reference data is version-controlled
- User-generated data is not committed to the repository
- Each deployment can have its own database instance
- The database can be reset to a known state at any time

## Deployment Considerations

For production deployments:

1. Set the `TINYDB_PATH` environment variable to specify a different database location
2. Run the initialization script to create the database with seed data
3. Consider implementing a backup strategy for user-generated data
4. For multi-instance deployments, consider using a shared database location

## Backup and Recovery

The `DatabaseHandler` class includes a `backup_database` method that creates a timestamped backup of the database file. This can be used for manual or scheduled backups.

To restore from a backup:
1. Stop the application
2. Copy the backup file to the location specified by `TINYDB_PATH`
3. Restart the application

## Future Improvements

Potential improvements to the database management approach:

1. Implement automatic scheduled backups
2. Add a command-line interface for database management tasks
3. Implement database migrations for schema changes
4. Add support for database encryption
5. Implement a more robust backup and recovery strategy 