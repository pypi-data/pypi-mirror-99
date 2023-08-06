/*
* Copyright © 2021 Contrast Security, Inc.
* See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
*/
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <funchook.h>

#include <contrast/assess/logging.h>
#include <contrast/assess/patches.h>
#include <contrast/assess/propagate.h>

#if PY_MAJOR_VERSION < 3
#define PY2
#endif /* PY_MAJOR_VERSION == 3 */

#define apply_or_fail(applyfunc, funchook)                          \
    do {                                                            \
        if ((applyfunc)((funchook)) != 0) {                         \
            /* Logging and exception is handled inside applyfunc */ \
            teardown_propagate();                                   \
            funchook_destroy((funchook));                           \
            return NULL;                                            \
        }                                                           \
    } while (0);


PyObject *set_attr_on_type(PyObject *self, PyObject *args) {
    PyTypeObject *type = NULL;
    PyObject *name = NULL;
    PyObject *attr = NULL;

    if (!PyArg_ParseTuple(args, "OOO", (PyObject **)&type, &name, &attr)) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse arguments");
        return NULL;
    }

    if (!PyType_Check(type)) {
        PyErr_SetString(PyExc_TypeError, "First argument must be a type");
        return NULL;
    }

    if (PyDict_SetItem(type->tp_dict, name, attr) != 0)
        return NULL;

    PyType_Modified(type);

    Py_RETURN_NONE;
}


PyObject *enable(PyObject *self, PyObject *args, PyObject *kwargs) {
    PyObject *logger = NULL;
    funchook_t *funchook = NULL;
    char *keywords[] = {"logger", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|O", keywords, &logger)) {
        /* Exception will propagate, no need to record to stderr */
        return NULL;
    }

    set_logger(logger);

    log_debug("BUILD DATETIME %s ", EXTENSION_BUILD_TIME);

    if (init_propagate() != 0) {
        /* Logging and exception occur inside init_propagate */
        return NULL;
    }

    log_debug("initialized propagation");

    if ((funchook = funchook_create()) == NULL) {
        log_exception(PyExc_RuntimeError, "failed to create funchook object");
        return NULL;
    }

    apply_or_fail(apply_cat_patch, funchook);
    apply_or_fail(apply_repeat_patch, funchook);
    apply_or_fail(apply_format_patch, funchook);
    apply_or_fail(apply_subscript_patch, funchook);
    apply_or_fail(apply_unicode_patches, funchook);
    apply_or_fail(apply_bytes_patches, funchook);
    apply_or_fail(apply_bytearray_patches, funchook);
    apply_or_fail(apply_stream_patches, funchook);
    apply_or_fail(apply_repr_patches, funchook);
#ifdef PY2
    apply_or_fail(apply_exec_patches, funchook);
    apply_or_fail(apply_cast_patches, funchook);
#endif

    if (funchook_install(funchook, 0) != FUNCHOOK_ERROR_SUCCESS) {
        log_exception(
            PyExc_RuntimeError,
            "failed to install assess patches: %s",
            funchook_error_message(funchook));
        funchook_destroy(funchook);
        return NULL;
    }

    log_debug("installed assess patches");

    return PyCapsule_New((void *)funchook, NULL, NULL);
}


PyObject *disable(PyObject *self, PyObject *arg) {

    funchook_t *funchook = NULL;

    if (!PyCapsule_IsValid(arg, NULL)) {
        log_exception(PyExc_TypeError, "Expected funchook container");
        return NULL;
    }

    if ((funchook = (funchook_t *)PyCapsule_GetPointer(arg, NULL)) == NULL) {
        log_exception(PyExc_RuntimeError, "Failed to get funchook from container");
        return NULL;
    }

    if (funchook_uninstall(funchook, 0) != FUNCHOOK_ERROR_SUCCESS) {
        log_exception(
            PyExc_RuntimeError,
            "Error uninstalling assess patches: %s",
            funchook_error_message(funchook));
        funchook_destroy(funchook);
        return NULL;
    }

    log_debug("uninstalled assess patches");

    teardown_propagate();

    log_debug("disabled propagation");

    funchook_destroy(funchook);

    teardown_logger();

    Py_RETURN_NONE;
}
