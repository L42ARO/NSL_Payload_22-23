#include "LinkedList.h"
#include <Arduino.h>

LinkedListNode::LinkedListNode(int value, LinkedListNode* previous, LinkedListNode* next)
    :Data(value),Previous(previous),Next(next){}

LinkedList::LinkedList()
    :Head(nullptr), Size(0){}
LinkedList::~LinkedList(){
    if(Head!=nullptr){
        LinkedListNode * Current = Head;
        while(Current->GetNext()!=nullptr){
            LinkedListNode * Temp = Current->GetNext();
            delete Current;
            Current = Temp;
        }
        delete Current;
        delete Head;
    }
}

void LinkedList::PushBack(int value){
    //Empty case
    if(Head == nullptr){
        Head = new LinkedListNode(value);
    }
    else{
        LinkedListNode * Current = Head;
        while (Current->GetNext() != nullptr)
        {
            Current = Current->GetNext();
        }
        LinkedListNode * Temp = new LinkedListNode(value, Current);
        Current->SetNext(Temp);
    }
    Size++;
}
void LinkedList::Pop(int idx){
    if(Head==nullptr) return; //TODO: Figure out a standard to report errors
    if(idx==0 && Head->GetNext()==nullptr){
        delete Head;
        Head = nullptr;
    }
    else if(idx==0){
        LinkedListNode * nxt = Head->GetNext();
        delete Head;
        Head = nxt;
    }
    else{
        LinkedListNode * Current = Head;
        int i;
        for(i=0;
            Current->GetNext()!=nullptr &&
            i!=idx;
            i++)
        {
            Current=Current->GetNext();
        }
        if(i!=idx) return;//Failed to get index to pop
        if(Current->GetNext()==nullptr){
            LinkedListNode * Prev = Current->GetPrev();
            Prev->SetNext(nullptr);
            delete Current;
        }
        else{
            LinkedListNode * prev = Current->GetPrev();
            prev->SetNext(Current->GetNext());
            delete Current;
        }
    }
    Size--;
}
int LinkedList::Get(int idx){
    if(Head==nullptr) return -6942;//NOT Possible to return NULL as an int value for Arduino
    if(idx==0) return Head->GetData();
    else{
        LinkedListNode * Current = Head;
        int i;
        for(i=0;
            i!= idx && Current->GetNext()!=nullptr;
            i++)
        {
            Current=Current->GetNext();
        }
        if(i!=idx) return -6942;//DID NOT FIND INDEX
        return Current->GetData();

    }
}