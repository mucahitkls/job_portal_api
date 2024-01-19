# Job Search API

## Introduction
Welcome to the Job Search API! This application is designed to streamline the process of job searching and posting. It allows users to create profiles, post job listings, apply for jobs, and manage applications. This API is built using FastAPI, with a PostgreSQL database for data storage, and it runs within a Vagrant-managed VirtualBox VM for easy setup and deployment.

## Technologies
- **FastAPI**: A modern, fast web framework for building APIs with Python.
- **PostgreSQL**: An advanced open-source relational database.
- **SQLAlchemy**: SQL toolkit and ORM for Python.
- **Vagrant**: A tool for building and managing virtual machine environments.
- **VirtualBox**: An open-source virtualization product.

## Setup and Installation

### Prerequisites
- Python 3.8+
- Vagrant 2.2+
- VirtualBox 6.1+

### Vagrant VM Setup
1. **Clone the Repository**: `git clone https://github.com/mucahitkls/job_portal_api.git`
2. **Navigate to Project Directory**: `cd db-setup`
3. **Start Vagrant VM**: Run `vagrant up`. This command sets up an Ubuntu VM, installs PostgreSQL, and configures the database.

### Database Configuration
The Vagrant setup script configures PostgreSQL as follows:
- Forwarding port `5432` to the host machine.
- Creating a PostgreSQL user `vagrant` with password `vagrant`.
- Creating a database `vagrant_db`.
- Setting up tables for users, jobs, and applications as per the SQL schema included in the repository.

### Application Setup
1. **Install Dependencies**: Run `pip install -r requirements.txt` to install the required Python packages.
2. **Set Database URL**: `export DATABASE_URL="postgresql://vagrant:vagrant@localhost:5432/vagrant_db"`.
3. **Start the Application**: `uvicorn app.main:app --reload`.

## Usage Guide for Job Search API

### Step 1: Starting the Application
- Run the FastAPI application with the command: `uvicorn app.main:app --reload`.
- This command starts the application and makes it accessible on `http://localhost:8000`.

### Step 2: Accessing the API Documentation
- Open a web browser and navigate to `http://localhost:8000/docs`.
- This page displays the Swagger UI documentation for the API, listing all available endpoints along with their request methods, parameters, and response formats.

### Step 3: User Registration
- Use the `/signup` endpoint to create a new user.
- Provide the necessary details like username, email, and password in the request body.

### Step 4: User Authentication
- Obtain an authentication token by using the `/token` endpoint.
- Submit the username and password in the request body.
- The response will include a JWT token which you'll use for authenticated requests.

### Step 5: Creating Job Listings
- Use the `/jobs/` POST endpoint to create a new job listing.
- Include job details such as title, description, employment type, and location in the request body.
- Ensure to include the JWT token obtained earlier in the request header for authentication.

### Step 6: Viewing Job Listings
- Retrieve all job listings using the `/jobs/` GET endpoint.
- Optionally, use query parameters `skip` and `limit` to paginate through the listings.

### Step 7: Applying for Jobs
- Use the `/applications/` POST endpoint to apply for a job.
- Provide the job ID and a cover letter in the request body.
- Include your authentication token in the request header.

### Step 8: Managing Applications
- View your applications using the `/applications/` GET endpoint.
- To update or delete an application, use the PUT and DELETE methods on the `/applications/{application_id}` endpoint.

### Step 9: Updating User and Job Information
- To update user information, use the PUT method on the `/users/{user_id}` endpoint.
- Similarly, update job listings using the PUT method on the `/jobs/{job_id}` endpoint.

### Step 10: Removing Entities
- Users and jobs can be deleted using the DELETE method on their respective endpoints.

## Contributing
Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.


Special thanks to the FastAPI community and contributors.

## Contact
For any inquiries or issues, please contact me at `kelessmucahit@gmail.com`.

---