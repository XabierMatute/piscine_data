# piscine_data

## Overview

**piscine_data** is a pedagogical project designed to introduce students to the fundamentals of data science. This unique initiative marks the first-ever intercampus collaborative correction system, fostering a sense of community and shared learning across multiple campuses. The project covers a wide range of topics, including database management, data cleaning, and Python programming, providing a solid foundation for further exploration in the field of data science.

This repository contains various exercises and scripts developed during the piscine, focusing on practical applications of data science concepts. While the project is still incomplete due to personal constraints, I am deeply honored to have participated in this groundbreaking first edition and look forward to completing it in the next iteration.

## Features

### Database Management
- **PostgreSQL Integration**:
  - Scripts for creating and managing tables (`items_table.py`, `customers_table.py`).
  - Data population using CSV files.
  - Removal of duplicates (`remove_duplicates.py`) and data fusion (`fusion.py`).
- **Dockerized Environment**:
  - Docker Compose setup for running PostgreSQL containers.
  - Scripts for connecting to and managing the database (`connect.sh`, `restore_database.sh`).

### Data Cleaning
- **Duplicate Removal**:
  - Scripts for identifying and removing duplicate entries in tables.
- **Data Fusion**:
  - Combining data from multiple tables to create unified datasets.

### Python Programming
- **Modular Design**:
  - Functions for creating tables, populating data, and handling errors.
- **Error Handling**:
  - Graceful management of database connection issues and invalid inputs.
- **File Parsing**:
  - Reading and validating CSV files for data population.

### Collaborative Learning
- **Intercampus Corrections**:
  - Leveraging feedback from peers across different campuses to improve solutions.
- **Shared Resources**:
  - Utilizing a centralized correction system to ensure consistency and quality.

## Code Structure

### Core Scripts
- **Database Management**:
  - [`items_table.py`](piscine_data/m01/Database/old_scripts/items_table.py): Handles the creation and population of the `items` table.
  - [`customers_table.py`](piscine_data/m02/Database/old_scripts/customers_table.py): Manages the `customers` table and its data.
  - [`remove_duplicates.py`](piscine_data/m02/Database/old_scripts/remove_duplicates.py): Removes duplicate entries from tables.
  - [`fusion.py`](piscine_data/m01/ex03/fusion.py): Combines data from multiple tables.

### Utilities
- **Connection Scripts**:
  - [`connect.sh`](piscine_data/m02/Database/connect.sh): Connects to the PostgreSQL database.
  - [`restore_database.sh`](piscine_data/m01/Database/restore_database.sh): Restores the database from CSV files.

### Configuration
- **Environment Variables**:
  - [`.env`](piscine_data/m01/Database/.env): Stores database credentials and container information.
- **Makefile**:
  - [`Makefile`](piscine_data/m02/Database/Makefile): Automates the setup and management of the Docker environment.

### Requirements
- **Python Dependencies**:
  - [`requirements.txt`](piscine_data/requirements.txt): Specifies required Python packages (`psycopg`).

## Competencies Involved

### Technical Skills
- **Database Management**: Creating, populating, and managing PostgreSQL tables.
- **Data Cleaning**: Removing duplicates and merging datasets.
- **Python Programming**: Writing modular and reusable scripts for data processing.
- **Docker**: Setting up and managing containerized environments.

### Problem-Solving
- **Error Handling**: Managing database connection issues and invalid inputs.
- **Optimization**: Ensuring efficient data processing and table management.
- **Collaboration**: Incorporating feedback from intercampus corrections.

### Personal Growth
- **Time Management**: Balancing personal commitments with project deadlines.
- **Learning**: Exploring new tools and techniques in data science.

## Reflections

Participating in the **piscine_data** has been an incredible honor. Being part of the first-ever intercampus collaborative correction system was a unique and inspiring experience. While personal circumstances prevented me from dedicating as much time as I would have liked, I am committed to completing this project during the next edition. This piscine has not only expanded my technical skills but also deepened my appreciation for collaborative learning and innovation.

## Disclaimer

**Important**: The `.env` file containing sensitive information, such as database credentials, has been included in this repository for educational purposes only. In a real-world or production project, **it is critical to never upload `.env` files or any sensitive credentials to a public repository**. Instead, use secure methods like environment variables or secret management tools.

## How to Run

1. Clone the repository.
2. Install Python dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up the Docker environment:
   ```sh
   make up
   ```
4. Restore the database:
   ```sh
   bash restore_database.sh
   ```
5. Run individual scripts as needed:
   ```sh
   python3 old_scripts/items_table.py <path_to_csv>
   ```

## Acknowledgments

Special thanks to the **42 School** for organizing this groundbreaking piscine and to the intercampus community for their invaluable feedback and support. I look forward to continuing this journey in the next edition.