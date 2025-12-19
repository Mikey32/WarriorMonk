from dataclasses import dataclass

@dataclass
class ActivityRow:
    date_val: str
    sleep: bool = False
    resistance: bool = False
    steps: int = 0
    sauna: bool = False
    cold_plunge: bool = False
    sprint: bool = False
    zone2cardio: bool = False
    meditation: bool = False
    core: bool = False
    mobility: bool = False

    @classmethod
    def from_sqlite_row(cls, row, default_values=None):
        """
        Convert a SQLite row tuple into an ActivityRow.
        Falls back to defaults if row is None.
        """
        if row:
            return cls(
                date_val=row[0],
                sleep=bool(row[1]),
                resistance=bool(row[2]),
                steps=row[3],
                sauna=bool(row[4]),
                cold_plunge=bool(row[5]),
                sprint=bool(row[6]),
                zone2cardio=bool(row[7]),
                meditation=bool(row[8]),
                core=bool(row[9]),
                mobility=bool(row[10]),
            )
        elif default_values:
            return cls(**default_values)
        else:
            raise ValueError("Row is None and no defaults provided")
