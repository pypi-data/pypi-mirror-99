#ifndef CDRIZZLEBLOT_H
#define CDRIZZLEBLOT_H

#include "cdrizzleutil.h"

/**
This routine does the interpolation of the input array.

@param[in,out] p A set of blotting parameters.  \a cblot_ provides an
example of one such way to do this.

@param[out] error

@return Non-zero if an error occurred.
*/
int
doblot(struct driz_param_t* p,
       struct driz_error_t* error);

#endif /* CDRIZZLEBLOT_H */
