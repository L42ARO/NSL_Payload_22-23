from gpiozero import Buzzer
import time
NOTE_B0 =  31
NOTE_C1 =  33
NOTE_CS1 = 35
NOTE_D1 =  37
NOTE_DS1 = 39
NOTE_E1 =  41
NOTE_F1 =  44
NOTE_FS1 = 46
NOTE_G1 =  49
NOTE_GS1 = 52
NOTE_A1 =  55
NOTE_AS1 = 58
NOTE_B1 =  62
NOTE_C2 =  65
NOTE_CS2 = 69
NOTE_D2 =  73
NOTE_DS2 = 78
NOTE_E2 =  82
NOTE_F2 =  87
NOTE_FS2 = 93
NOTE_G2 =  98
NOTE_GS2 = 104
NOTE_A2 =  110
NOTE_AS2 = 117
NOTE_B2 =  123
NOTE_C3 =  131
NOTE_CS3 = 139
NOTE_D3 =  147
NOTE_DS3 = 156
NOTE_E3 =  165
NOTE_F3 =  175
NOTE_FS3 = 185
NOTE_G3 =  196
NOTE_GS3 = 208
NOTE_A3 =  220
NOTE_AS3 = 233
NOTE_B3 =  247
NOTE_C4 =  262
NOTE_CS4 = 277
NOTE_D4 =  294
NOTE_DS4 = 311
NOTE_E4 =  330
NOTE_F4 =  349
NOTE_FS4 = 370
NOTE_G4 =  392
NOTE_GS4 = 415
NOTE_A4 =  440
NOTE_AS4 = 466
NOTE_B4 =  494
NOTE_C5 =  523
NOTE_CS5 = 554
NOTE_D5 =  587
NOTE_DS5 = 622
NOTE_E5 =  659
NOTE_F5 =  698
NOTE_FS5 = 740
NOTE_G5 =  784
NOTE_GS5 = 831
NOTE_A5 =  880
NOTE_AS5 = 932
NOTE_B5 =  988
NOTE_C6 =  1047
NOTE_CS6 = 1109
NOTE_D6 =  1175
NOTE_DS6 = 1245
NOTE_E6 =  1319
NOTE_F6 =  1397
NOTE_FS6 = 1480
NOTE_G6 =  1568
NOTE_GS6 = 1661
NOTE_A6 =  1760
NOTE_AS6 = 1865
NOTE_B6 =  1976
NOTE_C7 =  2093
NOTE_CS7 = 2217
NOTE_D7 =  2349
NOTE_DS7 = 2489
NOTE_E7 =  2637
NOTE_F7 =  2794
NOTE_FS7 = 2960
NOTE_G7 =  3136
NOTE_GS7 = 3322
NOTE_A7 =  3520
NOTE_AS7 = 3729
NOTE_B7 =  3951
NOTE_C8 =  4186
NOTE_CS8 = 4435
NOTE_D8 =  4699
NOTE_DS8 = 4978
melody = [
  NOTE_E7, NOTE_E7, 0, NOTE_E7,
  0, NOTE_C7, NOTE_E7, 0,
  NOTE_G7, 0, 0,  0,
  NOTE_G6, 0, 0, 0,

  NOTE_C7, 0, 0, NOTE_G6,
  0, 0, NOTE_E6, 0,
  0, NOTE_A6, 0, NOTE_B6,
  0, NOTE_AS6, NOTE_A6, 0,

  NOTE_G6, NOTE_E7, NOTE_G7,
  NOTE_A7, 0, NOTE_F7, NOTE_G7,
  0, NOTE_E7, 0, NOTE_C7,
  NOTE_D7, NOTE_B6, 0, 0,

  NOTE_C7, 0, 0, NOTE_G6,
  0, 0, NOTE_E6, 0,
  0, NOTE_A6, 0, NOTE_B6,
  0, NOTE_AS6, NOTE_A6, 0,

  NOTE_G6, NOTE_E7, NOTE_G7,
  NOTE_A7, 0, NOTE_F7, NOTE_G7,
  0, NOTE_E7, 0, NOTE_C7,
  NOTE_D7, NOTE_B6, 0, 0
]
tempo = [
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,

  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,

  9, 9, 9,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,

  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,

  9, 9, 9,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
]
melodyPin = 10
global buzzer
def setPin(pin):
  global buzzer
  melodyPin = pin
  buzzer = Buzzer(pin)
def sing(s):
    # iterate over the notes of the melody
    song = s
    if(song==1):

        print(" 'Mario Theme'")
        size = len(melody)
        for thisNote in range(size):

            # to calculate the note duration, take one second
            # divided by the note type.
            # e.g. quarter note = 1000 / 4, eighth note = 1000/8, etc.
            print(f'Note: {melody[thisNote]} Duration: {tempo[thisNote]}')
            noteDuration = 1000 // tempo[thisNote]

            buzz(melodyPin, melody[thisNote], noteDuration)

            # to distinguish the notes, set a minimum time between them.
            # the note's duration + 30% seems to work well:
            pauseBetweenNotes = noteDuration * 1.30
            time.sleep(pauseBetweenNotes/1000)

            # stop the tone playing:
            buzz(melodyPin, 0, noteDuration)


def buzz(targetPin, frequency, length):
    global buzzer
    delayValue = 1000000
    if(frequency != 0):
      delayValue /= frequency # calculate the delay value between transitions print(f'Delay01: {delayValue}')
    delayValue /= 2
    # 1 second's worth of microseconds, divided by the frequency, then split in half since
    # there are two phases to each cycle
    numCycles = frequency * length / 1000  # calculate the number of cycles for proper timing
    # multiply frequency, which is really cycles per second, by the number of seconds to
    # get the total number of cycles to produce
    for i in range(int(numCycles)):  # for the calculated length of time...
        buzzer.on()  # write the buzzer pin high to push out the diaphragm
        time.sleep(delayValue/1000000)  # wait for the calculated delay value
        buzzer.off()  # write the buzzer pin low to pull back the diaphragm
        time.sleep(delayValue/1000000)  # wait again or the calculated delay value

if __name__ == '__main__':
    setPin(10)
    sing(1)
