#include "InputToInt.h"

int InputToInt::inputToInt(String data){
    int numchar = data.length()-2;
    int moveamount =0;
    for (int i =0; numchar >0; numchar--, i++){
        moveamount += (data.charAt(2+i)-'0') * (pow(10, numchar-1));
    }
    return moveamount;
}
