Project Description:

This project is a Python-based web application built using the FastAPI framework, implementing a simple CRUD (Create, Read, Update, Delete) functionality with authentication and authorization features. The application allows users to sign up, log in, add posts, retrieve posts, and delete posts. It is designed following the MVC (Model-View-Controller) design pattern for better organization and maintainability.

Key Features:

- Signup and Login: Users can sign up for a new account and log in using their email and password. Authentication is implemented using JWT (JSON Web Tokens) for secure access.
  
- AddPost Endpoint: Authenticated users can add new posts, with validation to limit payload size. Each post is saved in memory, and a unique post ID is returned upon successful addition.
  
- GetPosts Endpoint: Authenticated users can retrieve all posts added by them. Response caching is implemented to improve performance by serving cached data for consecutive requests for up to 5 minutes.
  
- DeletePost Endpoint: Authenticated users can delete their posts by providing the post ID. The corresponding post is deleted from memory upon successful deletion.

### Technologies Used:

- Python: Core programming language used for backend development.
  
- FastAPI: A Modern web framework for building APIs with Python, providing high performance and ease of use.
  
- Pydantic: Data validation and settings management library used for defining Pydantic schemas for input validation.
  
- SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM) library used for interacting with the MySQL database.
  
- JWT (JSON Web Tokens): Authentication mechanism used for securing endpoints and validating user identity.

### Installation and Usage:

To run the application locally, clone the repository and install the required dependencies using pip. Then, configure the MySQL database connection and start the FastAPI server.

```bash
git clone https://github.com/timijab/Backend-dev-test.git
cd your_repository
pip install -r requirements.txt
uvicorn workspace:app --reload
```

For detailed instructions and documentation, refer to the project's README.md file.

### Contributing:

Contributions to the project are welcome! Feel free to open issues for bug reports, feature requests, or submit pull requests for enhancements or fixes.
