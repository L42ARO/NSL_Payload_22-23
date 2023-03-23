'''
    A1—Turn camera 60º to the right
    B2—Turn camera 60º to the left
    C3—Take picture
    D4—Change camera mode from color to grayscale
    E5—Change camera mode back from grayscale to color
    F6—Rotate image 180º (upside down).
    G7—Special effects filter (Apply any filter or image distortion you want and
    state what filter or distortion was used).
'''

# Default sequence will be A1, C3, B2, B2, D4, C3, A1, C3, A1, A1, A1, F6, C3
default_seq = ["A1", "C3", "B2", "B2", "D4", "C3", "A1", "C3", "A1", "A1", "A1", "F6", "C3"]
def GetRAFCOSequence():
    # Get the next sequence number for the RAF CO
    # Returns the next sequence number for the RAF CO
    seq = default_seq
    print(f'RAFCO sequence: {seq}')
    return seq