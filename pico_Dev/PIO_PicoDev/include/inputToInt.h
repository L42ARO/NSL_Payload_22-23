#ifndef INPUTTOINT_H
#define INPUTTOINT_H

#include <Arduino.h>



int inputToInt(String data){
    int numchar = data.length()-2;
    int moveamount =0;
    for (int i =0; numchar >0; numchar--, i++){
        moveamount += (data.charAt(2+i)-'0') * (pow(10, numchar-1));
    }
    return moveamount;
}

#endif // INPUTTOINT_H