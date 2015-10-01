#include "TObjArray.h"

class Formulas : public TObjArray {
  
  public:

  Bool_t Notify(){
    for(auto f: *this)
      f->Notify();
    return true;
  }

  ClassDef(Formulas,0);

};
