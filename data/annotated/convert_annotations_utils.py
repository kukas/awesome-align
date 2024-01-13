class Alignment:
    def __init__(self, index1, index2, type):
        self.pair = (index1, index2)
        if type.lower() in ["sure", "s", "-"]:
            self.type = "sure"
        elif type.lower() in ["possible", "p"]:
            self.type = "possible"
        else:
            raise ValueError("Invalid Alignment type"+type)
    @classmethod
    def from_string(cls, string, type=None):
        if type is None:
            if "p" in string:
                type = "p"
            else:
                type = "-"
        index1, index2 = string.split(type)
        return cls(int(index1), int(index2), type)

    def __repr__(self):
        if self.type == "sure":
            return f"{self.pair[0]}-{self.pair[1]}"
        elif self.type == "possible":
            return f"{self.pair[0]}p{self.pair[1]}"

    def __lt__(self, other):
        return self.pair < other.pair

    def __sub__(self, other):
        # check if other is int
        if isinstance(other, int):
            return Alignment(self.pair[0] - other, self.pair[1] - other, self.type)
        elif isinstance(other, tuple):
            assert len(other) == 2, f"other should be a tuple of length 2, but got {other}"
            return Alignment(self.pair[0] - other[0], self.pair[1] - other[1], self.type)
        else:
            raise NotImplementedError
    
    def __add__(self, other):
        # check if other is int
        if isinstance(other, int):
            return Alignment(self.pair[0] + other, self.pair[1] + other, self.type)
        elif isinstance(other, tuple):
            assert len(other) == 2, f"other should be a tuple of length 2, but got {other}"
            return Alignment(self.pair[0] + other[0], self.pair[1] + other[1], self.type)
        else:
            raise NotImplementedError

    def flip(self):
        return Alignment(self.pair[1], self.pair[0], self.type)

