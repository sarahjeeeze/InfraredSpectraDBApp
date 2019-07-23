# ftirdb
# Introduction

`ftirdb` is a ...

# Installation 

1. Create a new Python 3 environment `python3 -m venv ftirdb_env`
2. Enter the environment by running `./ftirdb_env/bin/activate`
3. Install and upgrade the packaging tools: `pip install --upgrade pip setuptools`
4. Install the project in editable mode `pip install -e ".[testing]"`
5. Create a new database
```bash
mysql -u root
create database mydb;
exit
```
6. Initialize and upgrade the database using Alembic: `alembic -c development.ini revision --autogenerate -m "init"`
7. Upgrade to that revision: `alembic -c development.ini upgrade head`
8. Load default data into the database using a script: `initialize_ftirdb_db development.ini`
9. Run your project's tests with `pytest`
10. Run your project `pserve development.ini`

