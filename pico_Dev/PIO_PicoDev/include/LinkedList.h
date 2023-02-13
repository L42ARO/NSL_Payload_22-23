#ifndef LINKED_LIST_H
#define LINKED_LIST_H
class LinkedListNode
{
public:
    LinkedListNode(int value,
                    LinkedListNode * previous = nullptr,
                    LinkedListNode * next = nullptr);
    LinkedListNode * GetNext() const{
        return Next;
    }
    LinkedListNode * SetNext(LinkedListNode * next){
        this->Next=next;
    }
    LinkedListNode * GetPrev() const{
        return Previous;
    }
    int GetData() const{
        return Data;
    }
private:
    int Data;
    LinkedListNode* Previous;
    LinkedListNode * Next;

};
class LinkedList
{
public:
    LinkedList();
    ~LinkedList();

    void PushBack(int value);
    void Pop(int idx=0);
    int Get(int idx=0);
    int operator[](int idx){
        return Get(idx);
    }
    int Length() const{
        return Size;
    }
private:
    LinkedListNode *Head;
    int Size;
};
#endif