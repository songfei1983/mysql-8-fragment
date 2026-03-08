# MySQL 8 Fragmentation Test

This project is designed to simulate, observe, and resolve table fragmentation in MySQL 8 using a table with a composite primary key. It includes scripts to generate large datasets, induce fragmentation through delete/insert cycles, and test online DDL operations to reclaim space.

## Prerequisites

- **Docker**: To run the MySQL 8 container.
- **Python 3**: To run the simulation scripts.
- **Python Libraries**:
  - `mysql-connector-python`

## Setup

1.  **Start the MySQL Container**:
    ```bash
    docker-compose up -d
    ```
    This will start a MySQL 8 instance and initialize the database `test_db` with the `composite_key_table`.

2.  **Install Python Dependencies**:
    ```bash
    pip install mysql-connector-python
    ```

## Usage

### 1. Initialize Data
Populate the table with a large initial dataset (approx. 40 million rows) to have a substantial base for fragmentation.
```bash
python insert_composite_key_table.py
```

### 2. Generate Fragmentation
Run the fragmentation simulation. This script repeatedly deletes and inserts rows in batches until the table's free space (data_free) exceeds 1GB.
```bash
python run_fragment_until.py
```
*Note: This process may take a significant amount of time depending on your hardware.*

### 3. Analyze & Fix Fragmentation
Run the online DDL test to rebuild the table and reclaim fragmented space. This script performs an `ALTER TABLE ... ENGINE=InnoDB` operation while concurrently running INSERT/SELECT queries to demonstrate online availability.
```bash
python alter_test.py
```

### Helper Scripts
- **Check Table Size**: View the current data size, index size, and free space of the table.
  ```bash
  python query_table_size.py
  ```
- **Single Fragmentation Cycle**: Run a single cycle of delete/insert operations (used internally by `run_fragment_until.py`).
  ```bash
  python fragment_test.py
  ```

## File Descriptions

- **`docker-compose.yml`**: Defines the MySQL 8 service configuration.
- **`init.sql`**: SQL script to create the `composite_key_table` with a complex primary key and multiple indexes.
- **`insert_composite_key_table.py`**: Multi-threaded script to insert a large volume of initial data.
- **`run_fragment_until.py`**: Main driver script that runs fragmentation cycles until a specific free space threshold is met.
- **`fragment_test.py`**: Performs batch deletions and insertions to cause fragmentation.
- **`alter_test.py`**: Tests `ALTER TABLE` for space reclamation and online DDL concurrency.
- **`query_table_size.py`**: Queries `information_schema.TABLES` to report table metrics.
