class Airplane:
    def __init__(self, country, name, speed_fly, altitude_fly):
        self._country = self.validate_str(country)
        self._name = self.validate_str(name)
        self._speed_fly = self.validate_num(speed_fly)
        self._altitude_fly = self.validate_num(altitude_fly)

    def validate_str(self, value):
        if not isinstance(value, str):
            return "UNKNOWN"
        clean_value = value.strip()
        if not clean_value:
            return "UNKNOWN"
        return clean_value

    def validate_num(self, value):
        try:
            return float(value)
        except ValueError, TypeError:
            return 0.0

    def __lt__(self, other):
        if not isinstance(other, Airplane):
            return NotImplemented
        return self._speed_fly < other._speed_fly

    def __eq__(self, other):
        if not isinstance(other, Airplane):
            return False
        return (
            self._speed_fly == other._speed_fly
            and self._altitude_fly == other._altitude_fly
        )
