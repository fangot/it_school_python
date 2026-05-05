import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple


class DBManager:
    def __init__(self, db_path: str) -> None:
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn: sqlite3.Connection = sqlite3.connect(str(db_path))
    
    def execute(self, sql: str, params: Tuple = ()) -> sqlite3.Cursor:
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        self.conn.commit()
        return cursor
    
    def fetch_one(self, sql: str, params: Tuple = ()) -> Optional[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        return dict(cursor.fetchone())
    
    def fetch_all(self, sql: str, params: Tuple = ()) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        result = []
        for row in cursor.fetchall():
            result.append(dict(row))
        return result
    
    def insert(self, table: str, data: Dict[str, Any], replace: bool = False) -> int:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        
        if replace:
            sql = f"INSERT OR REPLACE INTO {table} ({columns}) VALUES ({placeholders})"
        else:
            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        cursor = self.execute(sql, tuple(data.values()))
        return cursor.lastrowid
    
    def insert_many(self, table: str, rows: List[Dict[str, Any]], replace: bool = False) -> None:
        if not rows:
            return
        
        columns = ', '.join(rows[0].keys())
        placeholders = ', '.join(['?'] * len(rows[0]))
        
        if replace:
            sql = f"INSERT OR REPLACE INTO {table} ({columns}) VALUES ({placeholders})"
        else:
            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        values = []
        for row in rows:
            values.append(tuple(row.values()))
        #values = [tuple(row.values()) for row in rows]
        
        cursor = self.conn.cursor()
        cursor.executemany(sql, values)
        self.conn.commit()

    def select(self, table: str, cols: str = "*", where: Optional[str] = None, where_params: Tuple = (), extra: Optional[str] = None, extra_params: Tuple = ()) -> List[sqlite3.Row]:
        sql = f"SELECT {cols} FROM {table}"
        
        if where:
            sql += f" WHERE {where}"
        if extra:
            sql += f" {extra}"
        
        params = where_params + extra_params
        
        return self.fetch_all(sql, params)

    
    def create_table(self, table: str, cols: Dict[str, str], pk: Optional[str] = None) -> None:
        col_list = []
        for name, dtype in cols.items():
            col = f"{name} {dtype}"
            if pk and name == pk:
                col += " PRIMARY KEY"
            col_list.append(col)

        columns = ', '.join(col_list)
        
        self.execute(f"CREATE TABLE IF NOT EXISTS {table} ({columns})")
    
    def create_index(self, table: str, cols: List[str]) -> None:
        name = f"idx_{'_'.join(cols)}"
        columns = ', '.join(cols)
        self.execute(f"CREATE INDEX IF NOT EXISTS {name} ON {table} ({columns})")
    
    def count(self, table: str, where: Optional[str] = None, params: Tuple = ()) -> int:
        sql = f"SELECT COUNT(*) FROM {table}"
        
        if where:
            sql += f" WHERE {where}"
        
        result = self.fetch_one(sql, params)
        
        if result:
            return result[0]
        return 0
    
    def close(self) -> None:
        self.conn.close()
