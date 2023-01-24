#ifndef I2C_COM
#define I2C_COM
//MUST TRY TO MOVE THE COM_SYSTEM TO THIS HEADER FILE AND THEN TO IT'S OWN IMPLEMENTATION
class I2C_Comm {
  public:
    I2C_Comm();
    void begin();
    void loop();
    static void processCommand(int commandNumber, int value);
  private:
    static void receiveEvent(int howMany);
    static I2C_Comm* instance;
    static const uint8_t _address=8;
};
#endif