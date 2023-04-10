# TEST RESULS

The Arduino has a max ADC sample rate of around 8900 Hz

The Arduino UNO has a maximun sample rate of 8300 when reading from the A0 pin and putting it into the Serial port via binary bytes, sending it using Serial.println causes a lot of delay

To read from python is recommended the following:

```python
readings = [struct.unpack('>H', received_data[i] + received_data[i + 1])[0] for i in range(0, num_samples * 2, 2)]
```

## NOTES ON ANALOGREAD

Even though reading directly from the Analog pin produces faster results, they are not reliable values, so just use AnalogRead for reliable values.

Ways to test reilability:

- Connect A0 to GND, all values should be 0
- Connect A0 to 5v, all values should be 1023
- Connect A0 to 3.3v, all values should be around 674

## NOTES ON BAUD RATE

Using the AnalogRead function has proven to work well with 5000 baud rate, that's how we obtained 8300 Hz sample rate. Using anything below 1115200 baud is not recommended for RF purposes