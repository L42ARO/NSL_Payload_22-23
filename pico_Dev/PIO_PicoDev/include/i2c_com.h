#ifndef I2C_COM
#define I2C_COM

#include <Wire.h>

class I2C_Comm {
  public:
    static I2C_Comm& getInstance() {
      static I2C_Comm instance;
      return instance;
    }
    I2C_Comm() {};
    void begin(int address);
    static void processCommand(int commandNumber, int value);
  private:
    static void receiveEvent(int howMany);
    static I2C_Comm* instance;
    int _address;
};

#endif