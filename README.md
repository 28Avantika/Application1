# 3-Tier Rule Engine Application
A dynamic rule engine built with Python's Abstract Syntax Tree (AST) for flexible rule creation, modification, and execution.

# Overview
This project features a rule engine with a 3-tier architecture:

Frontend: Manages user interaction.
Backend: Processes rules and handles business logic using AST.
Database: Stores and manages rules.

# Installation
1. Clone the project and set up a virtual environment:

![image](https://github.com/user-attachments/assets/15d6d462-8c68-476c-a425-2a647bc2d28a)


2. Configure the database in config.py and initialize it:

python manage.py db upgrade

3. Start the application

   python app.py

# Usage
# Create a Rule
POST /api/rules
{
    "rule_name": "Check Age",
    "rule_expression": "age > 18"
}

# Execute a Rule
POST /api/rules/{rule_id}/execute
{
    "input_data": { "age": 25 }
}

# Configuration
Configure the following in config.py:

Database Connection, 
CORS Settings, 
Logging Options

# Directory Structure
![image](https://github.com/user-attachments/assets/255cb800-c062-4d85-a507-55142fe2f71a)

# Testing
pytest test_engine.py





   
