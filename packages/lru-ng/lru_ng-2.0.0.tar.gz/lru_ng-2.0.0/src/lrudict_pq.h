#ifndef LRUDICT_PQ_H
#define LRUDICT_PQ_H
#include "Python.h"
/* Simple queue supporting pushing to the end and claim-and-work by multiple
 * agents from the head; see CPython's Modules/_queuemodule.c for reference. */


#ifdef __GNUC__
extern PyObject * PyObject_CallFunctionObjArgs(PyObject *, ...)
__attribute__((sentinel));
#endif


struct _pq_sinfo {
    Py_ssize_t head;
    Py_ssize_t tail;
};


typedef struct _LRUDict_pq {
    struct _pq_sinfo sinfo;
    PyObject *lst;
    unsigned short n_active;
    unsigned short n_max;
} LRUDict_pq;

/* Hard-coded default n_max. */
#define LRUPQ_N_MAX_DEFAULT 8192

LRUDict_pq *
lrupq_new(void);

int
lrupq_free(LRUDict_pq *q);

Py_ssize_t
lrupq_purge(LRUDict_pq *q, PyObject *callback);

#endif
