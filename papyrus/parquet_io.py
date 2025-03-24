#!/bin/python
import os
from pathlib import Path
import pyarrow as pa
import pyarrow.dataset as ds
import pandas as pd

class ParquetRepository:

    def __init__(self, location):
        self.location = location

    def create_table_dir(self, table_dir: Path):
        """
        Create new directory for table to store parquet files
        ---
        Args:
        table_dir (Path): Path to the table directory
        """
        if not table_dir.parent.exists():
            raise FileNotFoundError(
                f"Parent directory {table_dir.parent} does not exist!!! (╯`Д´)╯︵ ┻━┻"
            )
        if table_dir.exists() and os.listdir(table_dir.as_posix()):
            raise FileExistsError(
                f"Directory {table_dir} already exists!!! (╯`Д´)╯︵ ┻━┻"
            )
        table_dir.mkdir(exist_ok=True)


    def write_data(self, table_dir:Path, data:pa.Table):
        """
        Write data to parquet file
        ---
        Args:
        table_dir (Path): Path to the table directory
        data (pa.Table): Data to write to the parquet file
        """
        if not table_dir.exists():
            raise FileNotFoundError(
                f"Directory {table_dir} does not exist!!! (╯`Д´)╯︵ ┻━┻"
            )
        new_data = data
        current_data = ds.dataset(table_dir.as_posix(), format="parquet").to_table()
        if current_data:
            new_data = pa.concat_tables([current_data, data])
        ds.write_dataset(
            new_data,
            table_dir.as_posix(),
            format="parquet",
            existing_data_behavior="delete_matching"
        )


    def read_data(self, table_dir:Path) -> pa.Table:
        """
        Read dataset from parquet files
        ---
        Args:
        table_dir (Path): Path to the table directory
        """
        if not table_dir.exists():
            raise FileNotFoundError(
                f"Directory {table_dir} does not exist!!! (╯`Д´)╯︵ ┻━┻"
            )
        return ds.dataset(table_dir.as_posix(), format="parquet").to_table()


    def delete_data_dir(self, table_dir:Path) -> pa.Table:
        """
        Delete directory with parquet files
        ---
        Args:
        table_dir (Path): Path to the table directory
        """
        if not table_dir.exists():
            raise FileNotFoundError(
                f"Directory {table_dir} does not exist!!! (╯`Д´)╯︵ ┻━┻"
            )
        data = ds.dataset(table_dir.as_posix(), format="parquet").to_table()
        table_dir.rmdir()
        return data

if __name__ == "__main__":
    pq_repo = ParquetRepository("/tmp/measurements")
    table_dir = Path("/Users/tranngocdangnguyen/Projects/papyrus/papyrus/tests/data/measurements")
    pq_repo.create_table_dir(table_dir)
    data = pa.Table.from_pandas(pd.DataFrame({"id": [1, 2, 3], "name": ["John", "Doe", "Smith"]}))
    pq_repo.write_data(table_dir, data)
    print(pq_repo.read_data(table_dir))
    print("="*20)
    print("append data")
    new_data = pa.Table.from_pandas(pd.DataFrame({"id": [4, 5, 6], "name": ["John", "Doe", "Smith"]}))
    pq_repo.write_data(table_dir, new_data)
    print(pq_repo.read_data(table_dir))
