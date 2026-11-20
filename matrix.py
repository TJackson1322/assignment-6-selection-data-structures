"""Matrix implementation using the custom DynamicArray."""

from data_structures import DynamicArray


class Matrix:
    """A rectangular matrix supporting row insertion and deletion."""

    def __init__(self, columns):
        if not isinstance(columns, int) or columns <= 0:
            raise ValueError("The number of columns must be positive.")

        # Each row must have this many columns to keep the matrix rectangular.
        self._columns = columns
        self._rows = DynamicArray()

    def shape(self):
        """Return the row and column counts in O(1) time."""
        return len(self._rows), self._columns

    def _check_column(self, column):
        if not 0 <= column < self._columns:
            raise IndexError("Column index out of range.")

    def get(self, row, column):
        """Access a cell in O(1) time."""
        self._check_column(column)
        # One array lookup finds the row. A second lookup finds the cell.
        return self._rows.get(row).get(column)

    def set(self, row, column, value):
        """Replace a cell in O(1) time."""
        self._check_column(column)
        self._rows.get(row).set(column, value)

    def insert_row(self, index, values):
        """Insert a row after checking its length.

        Copying the row costs O(c). Shifting row references costs
        O(r) in the worst case, for r rows and c columns.
        """
        if not 0 <= index <= len(self._rows):
            raise IndexError("Row insertion index out of range.")

        if len(values) != self._columns:
            raise ValueError(
                f"Each row must contain {self._columns} values."
            )

        # Copying the row prevents later edits to the input list from changing it.
        new_row = DynamicArray()

        for value in values:
            new_row.append(value)

        # Inserting a row shifts row references instead of copying every cell.
        self._rows.insert(index, new_row)

    def delete_row(self, index):
        """Remove a row and return its values in O(r + c) time."""
        removed = self._rows.delete(index)
        return removed.to_list()

    def to_list(self):
        """Return all values as nested lists in O(r * c) time."""
        return [
            self._rows.get(index).to_list()
            for index in range(len(self._rows))
        ]


def main():
    matrix = Matrix(3)
    matrix.insert_row(0, [1, 2, 3])
    matrix.insert_row(1, [4, 5, 6])

    print("Starting matrix:", matrix.to_list())
    print("Shape:", matrix.shape())
    print("Value at row 1, column 2:", matrix.get(1, 2))

    matrix.set(0, 1, 99)
    print("After changing a cell:", matrix.to_list())

    matrix.insert_row(1, [7, 8, 9])
    print("After inserting a row:", matrix.to_list())

    print("Deleted row:", matrix.delete_row(0))
    print("Final matrix:", matrix.to_list())


if __name__ == "__main__":
    main()
