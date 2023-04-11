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
    void begin(int address, void (*processCommand)(int commandNumber, int value));
    void setReady(int ready){
        _ready = ready;
    }
    
  private:
    static void receiveEvent(int howMany);
    static void requestEvent();
    static I2C_Comm* instance;
    int _address;
    int _ready;
    void (*processCommand)(int commandNumber, int value);

  static void sendEvent(String msg);
  
};

#endif