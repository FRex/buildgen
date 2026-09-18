#include <stdio.h>

static int myutf8main(int argc, char ** argv);
#define BLA_WMAIN_FUNC myutf8main
#include "blawmain.h"

static int myutf8main(int argc, char ** argv)
{
    fputs(argv[1], stdout);
    return 0;
}
