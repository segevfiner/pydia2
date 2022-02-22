#include <Python.h>
#include <Windows.h>
#include <dia2.h>
#include <diacreate.h>

static struct PyModuleDef _diamodule = {
    PyModuleDef_HEAD_INIT,
    "pydia2._dia",
    NULL,
    0,
    NULL
};

PyMODINIT_FUNC
PyInit__dia(void)
{
    PyObject* m = PyModule_Create(&_diamodule);
    if (!m) {
        return NULL;
    }

    PyObject* noRegCoCreatePtr = PyLong_FromVoidPtr(&NoRegCoCreate);
    if (!noRegCoCreatePtr) {
        Py_DECREF(m);
        return NULL;
    }

    if (PyModule_AddObject(m, "NoRegCoCreatePtr", noRegCoCreatePtr) < 0) {
        Py_DECREF(noRegCoCreatePtr);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
