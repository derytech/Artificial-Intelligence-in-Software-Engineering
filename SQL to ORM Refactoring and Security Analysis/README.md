# SQL to ORM Refactoring and Security Analysis

## Project Overview

This task demonstrates the refactoring of a database application from raw SQL to SQLAlchemy Object-Relational Mapping (ORM).

The purpose of the task is to understand how an ORM provides a higher level of abstraction between a Python application and a relational database. The original implementation uses raw SQL statements, while the refactored implementation uses SQLAlchemy models, an Engine, and an ORM Session.

## Files

* `initial_code.py` — The original implementation using raw SQL.
* `refactored_code.py` — The refactored implementation using SQLAlchemy ORM.
* `README.md` — Documentation and analysis of the refactoring.

## Original Raw SQL Approach

The initial implementation communicates directly with the database using SQL statements. Operations such as creating a table, inserting a user, retrieving a user, updating a user, deleting a user, and listing users are performed using SQL queries.

Although raw SQL provides direct control over the database, applications can become harder to maintain when SQL statements are spread throughout the Python code.

## SQLAlchemy ORM Approach

The refactored implementation uses SQLAlchemy ORM to represent database data as Python objects.

A `User` declarative class represents the users table. The model contains fields such as:

* `id`
* `username`
* `email`

SQLAlchemy's `Engine` provides the connection between the Python application and the database, while an ORM `Session` is used to manage database operations.

The application creates the database tables with:

```python
Base.metadata.create_all(engine)
```

The ORM implementation demonstrates the following operations:

1. Creating and adding a user.
2. Querying a user by username.
3. Updating a user.
4. Deleting a user.
5. Listing users.

## Abstraction

SQLAlchemy provides a higher level of abstraction because the developer can work with Python classes and objects instead of manually writing SQL statements for every database operation.

For example, instead of writing an SQL `INSERT` statement, the application can create a `User` object and add it to the SQLAlchemy session.

This allows the database structure to be represented directly in Python code and makes the application easier to understand.

## Security

Using SQLAlchemy ORM can help reduce SQL injection risks because database operations can be expressed through ORM methods rather than constructing SQL queries by directly concatenating user-provided values into SQL strings.

However, using an ORM does not automatically make an application completely secure. Developers must still validate input, manage authentication and authorization properly, protect database credentials, and follow secure coding practices.

## Maintainability

The ORM approach improves maintainability by keeping the database structure in Python model classes and reducing repetitive SQL code.

If the application grows and additional fields or database relationships are required, the models can be extended in a structured way. This can make the application easier to test, modify, and expand.

## Raw SQL vs ORM

| Feature              | Raw SQL                                      | SQLAlchemy ORM                                    |
| -------------------- | -------------------------------------------- | ------------------------------------------------- |
| Database interaction | SQL statements                               | Python objects and ORM methods                    |
| Abstraction level    | Lower                                        | Higher                                            |
| Readability          | Can become difficult as queries increase     | Often easier to understand in Python applications |
| Maintainability      | SQL may be spread throughout the application | Models centralize database structure              |
| SQL injection risk   | Requires careful parameterization            | ORM methods can reduce risks when used correctly  |
| Database control     | Direct control over SQL                      | ORM manages much of the SQL generation            |
| Learning curve       | Requires SQL knowledge                       | Requires understanding of ORM concepts            |

## Conclusion

The refactoring demonstrates how SQLAlchemy ORM can provide a cleaner and more maintainable approach to database programming. Instead of managing SQL statements throughout the application, developers can work with Python classes and objects while SQLAlchemy handles much of the interaction with the relational database.

Raw SQL is still useful when developers need precise control over database queries or complex database-specific operations. However, for many Python applications, SQLAlchemy ORM provides a useful balance between abstraction, readability, security, and maintainability.
