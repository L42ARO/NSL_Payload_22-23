# Default sequence will be A1, C3, B2, B2, D4, C3, A1, C3, A1, A1, A1, F6, C3
default_seq = ["A1", "C3", "B2", "B2", "D4", "C3", "A1", "C3", "A1", "A1", "A1", "F6", "C3"]
def GetRAFCOSequence():
    # Get the next sequence number for the RAF CO
    # Returns the next sequence number for the RAF CO
    seq = default_seq
    print(f'RAFCO sequence: {seq}')
    return seq