#include "Python.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <complex.h>

#define NO_IMPORT_ARRAY
#define PY_ARRAY_UNIQUE_SYMBOL gofast_ARRAY_API
#include "numpy/arrayobject.h"

#include "readers.h"

/*
  TBW Reader (12-bit and 4-bit samples)
*/

#pragma pack(push)
#pragma pack(1)
typedef struct {
    unsigned int sync_word;
    union {
        struct {
            unsigned int frame_count:24;
            unsigned char id:8;
        };
        unsigned int frame_count_word;
    };
    unsigned int second_count;
    union {
        unsigned short int tbw_id;
        struct {
            unsigned short int stand:14;
            unsigned char bits:1;
            unsigned char is_tbw:1;
        };
    };
    unsigned short int unassigned;
} TBWHeader;


typedef struct {
    unsigned long long timetag;
    unsigned char bytes[1200];
} TBWPayload;


typedef struct {
    TBWHeader header;
    TBWPayload payload;
} TBWFrame;
#pragma pack(pop)


PyObject *tbw_method = NULL;
PyObject *tbw_size   = NULL;


PyObject *read_tbw(PyObject *self, PyObject *args) {
    PyObject *ph, *buffer, *output, *frame, *fHeader, *fPayload, *temp;
    PyArrayObject *data4, *data12;
    int i;
    TBWFrame cFrame;
    
    if(!PyArg_ParseTuple(args, "OO", &ph, &frame)) {
        PyErr_Format(PyExc_RuntimeError, "Invalid parameters");
        return NULL;
    }
    
    // Create the output data arrays
    // 4-bit
    npy_intp dims[2];
    dims[0] = (npy_intp) 2;
    dims[1] = (npy_intp) 1200;
    data4 = (PyArrayObject*) PyArray_ZEROS(2, dims, NPY_INT16, 0);
    // 12-bit
    dims[0] = (npy_intp) 2;
    dims[1] = (npy_intp) 400;
    data12 = (PyArrayObject*) PyArray_ZEROS(2, dims, NPY_INT16, 0);
    if( data4 == NULL || data12 == NULL ) {
        PyErr_Format(PyExc_MemoryError, "Cannot create output array");
        goto fail;
    }
    
    // Read from the file
    if( tbw_method == NULL ) {
        tbw_method = Py_BuildValue("s", "read");
        tbw_size = Py_BuildValue("i", sizeof(cFrame));
    }
    buffer = PyObject_CallMethodObjArgs(ph, tbw_method, tbw_size, NULL);
    if( buffer == NULL ) {
        if( PyObject_HasAttrString(ph, "read") ) {
            PyErr_Format(PyExc_IOError, "An error occured while reading from the file");
        } else {
            PyErr_Format(PyExc_AttributeError, "Object does not have a read() method");
        }
        goto fail;
    } else if( PyString_GET_SIZE(buffer) != sizeof(cFrame) ) {
        PyErr_Format(EOFError, "End of file encountered during filehandle read");
        goto fail;
    }
    memcpy(&cFrame, PyString_AS_STRING(buffer), sizeof(cFrame));
    Py_XDECREF(buffer);
    
    Py_BEGIN_ALLOW_THREADS
    
    // Swap the bits around
    cFrame.header.frame_count_word = __bswap_32(cFrame.header.frame_count_word);
    cFrame.header.second_count = __bswap_32(cFrame.header.second_count);
    cFrame.header.tbw_id = __bswap_16(cFrame.header.tbw_id);
    cFrame.payload.timetag = __bswap_64(cFrame.payload.timetag);
    
    // Fill the data array
    if(cFrame.header.bits == 0) {
        short int tempR;
        short int *a;
        a = (short int *) PyArray_DATA(data12);
        for(i=0; i<400; i++) {
            tempR = (cFrame.payload.bytes[3*i]<<4) | ((cFrame.payload.bytes[3*i+1]>>4)&15);
            tempR -= ((tempR&2048)<<1);
            *(a + i) = (short int) tempR;

            tempR = ((cFrame.payload.bytes[3*i+1]&15)<<8) | cFrame.payload.bytes[3*i+2];
            tempR -= ((tempR&2048)<<1);
            *(a + 400 + i) = (short int) tempR;
        }
    } else {
        const short int *fp;
        short int *a;
        a = (short int *) PyArray_DATA(data4);
        for(i=0; i<1200; i++) {
            fp = tbw4LUT[ cFrame.payload.bytes[i] ];
            *(a + i) = (short int) fp[0];
            *(a + 1200 + i) = (short int) fp[1];
        }
    }
    
    Py_END_ALLOW_THREADS
    
    // Validate
    if( !validSync5C(cFrame.header.sync_word) ) {
        PyErr_Format(SyncError, "Mark 5C sync word differs from expected");
        goto fail;
    }
    
    // Save the data to the frame object
    // 1.  Header
    fHeader = PyObject_GetAttrString(frame, "header");
    temp = PyLong_FromUnsignedLong(cFrame.header.frame_count);
    PyObject_SetAttrString(fHeader, "frame_count", temp);
    Py_XDECREF(temp);
    
    temp = PyLong_FromUnsignedLong(cFrame.header.second_count);
    PyObject_SetAttrString(fHeader, "second_count", temp);
    Py_XDECREF(temp);
    
    temp = Py_BuildValue("H", cFrame.header.tbw_id);
    PyObject_SetAttrString(fHeader, "tbw_id", temp);
    Py_XDECREF(temp);
    
    // 2. Data
    fPayload = PyObject_GetAttrString(frame, "payload");
    
    temp = PyLong_FromUnsignedLongLong(cFrame.payload.timetag);
    PyObject_SetAttrString(fPayload, "timetag", temp);
    Py_XDECREF(temp);
    
    if(cFrame.header.bits == 0) {
        PyObject_SetAttrString(fPayload, "_data", PyArray_Return(data12));
    } else {
        PyObject_SetAttrString(fPayload, "_data", PyArray_Return(data4));
    }
    
    // 3. Frame
    PyObject_SetAttrString(frame, "header", fHeader);
    PyObject_SetAttrString(frame, "payload", fPayload);
    output = Py_BuildValue("O", frame);
    
    Py_XDECREF(fHeader);
    Py_XDECREF(fPayload);
    Py_XDECREF(data4);
    Py_XDECREF(data12);
    
    return output;
    
fail:
    Py_XDECREF(data4);
    Py_XDECREF(data12);
    
    return NULL;
}

char read_tbw_doc[] = PyDoc_STR(\
"Function to read in a single TBW frame (header+payload) and store the contents\n\
as a Frame object.\n\
");
