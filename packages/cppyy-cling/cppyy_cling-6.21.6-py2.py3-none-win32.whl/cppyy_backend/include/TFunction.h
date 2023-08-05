// @(#)root/meta:$Id$
// Author: Fons Rademakers   07/02/97

/*************************************************************************
 * Copyright (C) 1995-2000, Rene Brun and Fons Rademakers.               *
 * All rights reserved.                                                  *
 *                                                                       *
 * For the licensing terms see $ROOTSYS/LICENSE.                         *
 * For the list of contributors see $ROOTSYS/README/CREDITS.             *
 *************************************************************************/

#ifndef ROOT_TFunction
#define ROOT_TFunction

//////////////////////////////////////////////////////////////////////////
//                                                                      //
// TFunction                                                            //
//                                                                      //
// Dictionary of global functions.                                      //
//                                                                      //
//////////////////////////////////////////////////////////////////////////

#include "TDictionary.h"


namespace CppyyLegacy {

class TFunction : public TDictionary {

friend class TCling;

protected:
   MethodInfo_t   *fInfo;            //pointer to Interpreter function info
   TString         fMangledName;     //Mangled name as determined by CINT.
   std::string     fRTName;
   std::string     fRTNormName;
   TList          *fMethodArgs;      //list of function arguments

public:
   TFunction(MethodInfo_t *info = 0);
   TFunction(const TFunction &orig);
   TFunction& operator=(const TFunction &rhs);
   virtual            ~TFunction();
   virtual TObject    *Clone(const char *newname="") const;
   virtual const char *GetMangledName() const;
   const char         *GetReturnTypeName() const;
   std::string         GetReturnTypeNormalizedName() const;
   TList              *GetListOfMethodArgs();
   Int_t               GetNargs() const;
   Int_t               GetNargsOpt() const;
   DeclId_t            GetDeclId() const;
   void               *InterfaceMethod(bool as_iface) const;
   virtual Bool_t      IsValid();
   Long_t              Property() const;
   Long_t              ExtraProperty() const;
   virtual bool        Update(MethodInfo_t *info);

   ClassDef(TFunction,0)  //Dictionary for global function
};

} // namespace CppyyLegacy
#endif
