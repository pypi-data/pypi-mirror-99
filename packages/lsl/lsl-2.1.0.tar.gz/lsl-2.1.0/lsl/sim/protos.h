/*   
 *     From the SciPi GitHub Repository
 *     https://github.com/scipy/scipy/blob/master/scipy/special/cephes/
 */

#ifndef __SCIPY_SPECIAL_CEPHES
#define __SCIPY_SPECIAL_CEPHES

/* Complex numeral.  */
typedef struct {
    double r;
    double i;
} cmplx;

extern double j1(double x);
extern double y1(double x);

extern int mtherr(char *name, int code);

extern double polevl(double x, double *P, int N);
extern double p1evl(double x, double *P, int N);

#endif
