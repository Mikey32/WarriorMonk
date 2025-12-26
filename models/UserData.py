from dataclasses import dataclass

@dataclass
class UserData:
    name: str
    experience: int = 0
    level: int = 0
    last_weekly_bonus: str

    @classmethod
    def from_sqlite_row(cls, row, default_values=None):
        """
        Convert a SQLite row tuple into a UserData instance.
        Falls back to defaults if row is None.
        """
        if row:
            return cls(
                name=row[0],
                experience=row[1],
                level=row[2],
                last_weekly_bonus=row[3],
            )
        elif default_values:
            return cls(**default_values)
        else:
            raise ValueError("Row is None and no defaults provided")

    @classmethod
    def columns(cls):
        return ("name", "experience", "level", "last_weekly_bonus")

    def to_tuple(self):
        return (self.name, self.experience, self.level, self.last_weekly_bonus)