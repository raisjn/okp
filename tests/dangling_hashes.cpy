#include <stdio.h>

did_setup := false

int main():
  #ifdef DEV
  return 0
  #else
  return 1
  #endif

def foo():
  pass

namespace bar:
  void setup_font():
    if !did_setup:
      const char *filename = "blahblah"
      if filename == "":
        #ifndef REMARKABLE
        filename = "blah"
       // TODO: fix the max size read to prevent overflows (or just abort on really large files)
        #else
        filename = "balh"
        #endif
