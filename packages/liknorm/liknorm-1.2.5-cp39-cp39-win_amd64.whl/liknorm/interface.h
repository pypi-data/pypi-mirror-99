struct LikNormMachine;

enum Lik {
    BERNOULLI,
    BINOMIAL,
    POISSON,
    EXPONENTIAL,
    GAMMA,
    GEOMETRIC,
    PROBIT,
    NBINOMIAL
};

struct LikNormMachine *create_machine(int);
void apply1d(struct LikNormMachine *, enum Lik, int, double *, double *,
             double *, double *, double *, double *);
void apply2d(struct LikNormMachine *, enum Lik, int, double *, double *,
             double *, double *, double *, double *, double *);
void destroy_machine(struct LikNormMachine *);
int allfinite(int size, double const *arr);
