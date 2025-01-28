# piece.py

class Piece:
    def __init__(self, rank, player):
        self.rank = rank  # Rank can be an integer or string based on piece type
        self.revealed = False
        self.move_history = []
        self.player = player
        self.is_movable = True  # Default to movable

        # Set immobility for Bomb and flag
        if self.rank == 'B' or self.rank == 'F':
            self.is_movable = False

    def __str__(self):
        return str(self.rank) if self.revealed else "?"

    def __repr__(self):
        return f"Piece({self.rank}, {self.player})"
    
    def __hash__(self):
        return hash((self.rank, self.player))

    def __eq__(self, other):
        if isinstance(other, Piece):
            return self.compare(other) == 0
        return False

    def __lt__(self, other):
        if isinstance(other, Piece):
            return self.compare(other) < 0
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Piece):
            return self.compare(other) <= 0
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Piece):
            return self.compare(other) > 0
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Piece):
            return self.compare(other) >= 0
        return NotImplemented

    def compare(self, other):
        """
        Compare two pieces based on their rank (either string or int).
        Returns:
        -1 if self is less than other,
         0 if equal,
         1 if self is greater than other.
        """
        # Handle comparison with 'B' (Bomb) and 'F' (Flag)
        if isinstance(self.rank, int) and isinstance(other.rank, int):
            # Integer vs Integer
            return self.rank - other.rank
        elif isinstance(self.rank, int) and isinstance(other.rank, str):
            if other.rank == 'B':
                # Bomb beats all ranks except 3
                return -1 if self.rank != 3 else 0
            elif other.rank == 'F':
                # Flag beats all ranks
                return 1
        elif isinstance(self.rank, str) and isinstance(other.rank, int):
            if self.rank == 'B':
                # Bomb beats all ranks except 3
                return 1 if other != 3 else 0
            elif self.rank == 'F':
                # Flag beats all ranks
                return -1
        elif isinstance(self.rank, str) and isinstance(other.rank, str):
            # String vs String comparison ('F' vs 'B')
            if self.rank == 'F' and other.rank == 'B':
                return 1
            elif self.rank == 'B' and other.rank == 'F':
                return -1
            return 0

        return 0