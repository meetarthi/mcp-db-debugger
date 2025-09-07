# mcp-db-debugger

**Overview**

MCP Database Debugger is a database troubleshooting tool that combines the power of OpenAI's GPT-4 with database interactions through the MCP. It analyzes database errors, executes safe diagnostic queries, and provides actionable recommendations to resolve issues quickly.

**Integration Flow:**

1. User Input → Streamlit UI
2. AI Analysis → OpenAI processes error and generates diagnostic queries
3. Security Check → MCP validates queries are safe(no DML operations)
4. Database Execution → MCP runs approved queries
5. Result Synthesis → Combined AI analysis + database results = actionable recommendations



**Creating DB in terminal and getting the error for debugger :*
1. Install MySQL

   ```
brew install mysql 
   ```

2.Start MySQL and log in as root:

```
mysql -u root -p
```

3.Create the database:

```
create database order_db;
```

4. Create a new user and grant privileges:

```
CREATE USER 'your_username'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON your_database_name.* TO 'your_username'@'localhost';
```

5. Install jupyterlab

```
pip install jupyterlab
```

6. Run the notebook in the repo to get the error generated from the DB



**How to run:**
1. Clone the repo -

```
git clone https://github.com/meetarthi/mcp-db-debugger.git
```

2. Create a virtual environment 

```
python -m venv [env_name]
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Replace openAI key and DB details in .env file

```
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=mysql://[user]:[username]@localhost/[Db_name]
```
