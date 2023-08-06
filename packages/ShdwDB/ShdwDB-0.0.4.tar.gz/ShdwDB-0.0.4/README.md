# The ShdwDB package
This package is for databases and storage.
Use it to create tables with rows and columns.
## Functions
### `make(name, column_names, row_names)`
This creates a new database. `column_names` must be an iterable containing the names of the columns. `row_names` must be also be an iterable with the row names.
### `retrieve(name, key_saved)`
Retrive a database from the replit db storage. Give it a name and specifiy the key you saved it with.
## Database methods
+ `set(column, row, value)`: Set a value to a cell.
+ `delete_item(column, row)`: Set the cell value to None.
+ `delete_column(column)`: Delete the column.
+ `delete_row(row)`: Delete the row.
+ `get_value(column, row)`: Get the value of a cell.
+ `get_column(column)`: Get a column.
+ `get_row(row)`: Get a row(as a string).
+ `save(key_to_save)`: Save the Database to replit db.
+ `add_column(name)`: Add a column.
+ `add_row(name)`: Add a row.