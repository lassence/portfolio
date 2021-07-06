# Import foreign PostgreSQL database

PostgreSQL provides a useful feature called Foreign Data Wrapper, that can be used to access data stored on external PostgreSQL servers. On Postgres 9.3+, an extension named `postgres_fdw` enables this feature (see [documentation](https://www.postgresql.org/docs/current/postgres-fdw.html)). 

## Install extension

```sql
CREATE EXTENSION IF NOT EXISTS postgres_fdw;
```

## Create foreign server

```sql
/* Optional: drop existing server */
DROP SERVER IF EXISTS external_server CASCADE;

/* Create server 'external_server' */
        CREATE SERVER external_server
 FOREIGN DATA WRAPPER postgres_fdw
              OPTIONS (host 'host.example.com', dbname 'db_name', port '5432');
```

## Create user mapping

```sql
/* Optional: drop existing user mapping */
  DROP USER MAPPING IF EXISTS 
   FOR CURRENT_USER 
SERVER external_server;

/* Create user mapping for current user*/
 CREATE USER MAPPING 
    FOR CURRENT_USER
 SERVER external_server
OPTIONS (user 'user', password 'password');
```

## Import external tables

```sql
/* Create a schema for imported tables */
CREATE SCHEMA IF NOT EXISTS import;
```

If you want to import the full foreign schema:

```sql
/* Import full external server schema 'public' into local schema 'import' */
IMPORT FOREIGN SCHEMA public
          FROM SERVER external_server
                 INTO import;
```

If you want to import only some tables:

```sql
/* Optional: drop existing local table */
DROP FOREIGN TABLE IF EXISTS import.categories;

/* Import external table 'public.categories' to table 'import.categories' */
CREATE FOREIGN TABLE import.categories (
    id            integer,
    name          varchar,
    parent_id     integer,
    type          varchar,
    description   text
) 
 SERVER external_server
OPTIONS (schema_name 'public', table_name 'categories');

/* Optional: check new table */
SELECT *
  FROM import.categories
 LIMIT 10
```

## List current foreign resources

```sql
/* List foreign servers */
SELECT srvname,
       srvowner::regrole,
       fdwname,
       srvoptions
  FROM pg_foreign_server
  JOIN pg_foreign_data_wrapper AS w 
    ON w.oid = srvfdw;
```

```sql
/* List foreign tables */
SELECT * 
  FROM information_schema.foreign_tables
```

```sql
/* List users mappings */
SELECT *
  FROM pg_catalog.pg_user_mappings
```

