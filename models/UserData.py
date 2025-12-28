from dataclasses import dataclass

@dataclass
class UserData:
    name: str
    experience: int = 0
    level: int = 0

    @classmethod
    def from_sqlite_row(cls, row, default_values=None):
        """
        Convert a SQLite row tuple into a UserData instance.
        Falls back to defaults if row is None.
        """
        if row:
            return cls(
                name=row[0],
                level=row[1],
                experience=row[2],
            )
        elif default_values:
            return cls(**default_values)
        else:
            raise ValueError("Row is None and no defaults provided")

    @classmethod
    def columns(cls):
        return ("name", "experience", "level")

    def to_tuple(self):
        return (self.name, self.experience, self.level)