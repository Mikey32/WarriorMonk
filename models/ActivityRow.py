from dataclasses import dataclass

@dataclass
class ActivityRow:
    date_val: str
    sleep: str
    resistance: bool = False
    steps: int = 0
    sauna: bool = False
    cold_plunge: bool = False
    sprint: bool = False
    zone2cardio: int = 0
    meditation: int = 0
    hiit: int = 0
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
                sleep=row[1],
                resistance=bool(row[2]),
                steps=row[3],
                sauna=bool(row[4]),
                cold_plunge=bool(row[5]),
                sprint=bool(row[6]),
                zone2cardio=row[7],
                meditation=row[8],
                hiit=row[9],
                mobility=bool(row[10]),
            )
        elif default_values:
            return cls(**default_values)
        else:
            raise ValueError("Row is None and no defaults provided")
    def to_tuple(self):
        return (
            self.date_val,
            self.sleep,
            self.resistance,
            self.steps,
            self.sauna,
            self.cold_plunge,
            self.sprint,
            self.zone2cardio,
            self.meditation,
            self.hiit,
            self.mobility,
        )
    
    @classmethod
    def columns(cls):
        return (
            "date_val",
            "sleep",
            "resistance",
            "steps",
            "sauna",
            "cold_plunge",
            "sprint",
            "zone2cardio",
            "meditation",
            "hiit",
            "mobility",
        )

