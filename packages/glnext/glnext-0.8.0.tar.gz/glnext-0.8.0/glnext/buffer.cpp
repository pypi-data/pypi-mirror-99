#include "glnext.hpp"

Buffer * Instance_meth_buffer(Instance * self, PyObject * vargs, PyObject * kwargs) {
    static char * keywords[] = {
        "type",
        "size",
        "readable",
        "writable",
        "memory",
        NULL,
    };

    struct {
        PyObject * type;
        VkDeviceSize size;
        VkBool32 readable = false;
        VkBool32 writable = true;
        PyObject * memory = Py_None;
    } args;

    int args_ok = PyArg_ParseTupleAndKeywords(
        vargs,
        kwargs,
        "O!K|$ppO",
        keywords,
        &PyUnicode_Type,
        &args.type,
        &args.size,
        &args.readable,
        &args.writable,
        &args.memory
    );

    if (!args_ok) {
        return NULL;
    }

    VkBufferUsageFlags buffer_usage = 0;

    if (!PyUnicode_CompareWithASCIIString(args.type, "vertex_buffer")) {
        buffer_usage = VK_BUFFER_USAGE_VERTEX_BUFFER_BIT;
    }

    if (!PyUnicode_CompareWithASCIIString(args.type, "instance_buffer")) {
        buffer_usage = VK_BUFFER_USAGE_VERTEX_BUFFER_BIT;
    }

    if (!PyUnicode_CompareWithASCIIString(args.type, "index_buffer")) {
        buffer_usage = VK_BUFFER_USAGE_INDEX_BUFFER_BIT;
    }

    if (!PyUnicode_CompareWithASCIIString(args.type, "indirect_buffer")) {
        buffer_usage = VK_BUFFER_USAGE_INDIRECT_BUFFER_BIT;
    }

    if (!PyUnicode_CompareWithASCIIString(args.type, "storage_buffer")) {
        buffer_usage = VK_BUFFER_USAGE_STORAGE_BUFFER_BIT;
    }

    if (!PyUnicode_CompareWithASCIIString(args.type, "uniform_buffer")) {
        buffer_usage = VK_BUFFER_USAGE_UNIFORM_BUFFER_BIT;
    }

    if (!buffer_usage) {
        PyErr_Format(PyExc_ValueError, "type");
        return NULL;
    }

    if (args.readable) {
        buffer_usage |= VK_BUFFER_USAGE_TRANSFER_SRC_BIT;
    }

    if (args.writable) {
        buffer_usage |= VK_BUFFER_USAGE_TRANSFER_DST_BIT;
    }

    Memory * memory = get_memory(self, args.memory);

    Buffer * res = new_buffer({
        self,
        memory,
        args.size,
        buffer_usage,
    });

    allocate_memory(memory);
    bind_buffer(res);
    return res;
}

PyObject * Buffer_meth_read(Buffer * self) {
    HostBuffer temp = {};
    VkDeviceSize offset = 0;
    if (self->instance->group) {
        temp = self->instance->group->temp;
        temp.ptr = (char *)temp.ptr + self->instance->group->offset;
        offset = self->instance->group->offset;
    } else {
        new_temp_buffer(self->instance, &temp, self->size);
        begin_commands(self->instance);
    }

    VkBufferCopy copy = {0, offset, self->size};
    self->instance->vkCmdCopyBuffer(
        self->instance->command_buffer,
        self->buffer,
        temp.buffer,
        1,
        &copy
    );

    if (self->instance->group) {
        PyObject * mem = PyMemoryView_FromMemory((char *)temp.ptr, self->size, PyBUF_READ);
        PyList_Append(self->instance->group->output, mem);
        Py_DECREF(mem);
        self->instance->group->offset += self->size;
        Py_RETURN_NONE;
    }

    end_commands(self->instance);
    PyObject * res = PyBytes_FromStringAndSize((char *)temp.ptr, self->size);
    free_temp_buffer(self->instance, &temp);
    return res;
}

PyObject * Buffer_meth_write(Buffer * self, PyObject * arg) {
    Py_buffer view = {};
    if (PyObject_GetBuffer(arg, &view, PyBUF_STRIDED_RO)) {
        return NULL;
    }

    if ((VkDeviceSize)view.len > self->size) {
        PyErr_Format(PyExc_ValueError, "wrong size");
        return NULL;
    }

    HostBuffer temp = {};
    VkDeviceSize offset = 0;
    if (self->instance->group) {
        temp = self->instance->group->temp;
        temp.ptr = (char *)temp.ptr + self->instance->group->offset;
        offset = self->instance->group->offset;
    } else {
        new_temp_buffer(self->instance, &temp, self->size);
        begin_commands(self->instance);
    }

    PyBuffer_ToContiguous(temp.ptr, &view, view.len, 'C');
    PyBuffer_Release(&view);

    VkBufferCopy copy = {offset, 0, self->size};
    self->instance->vkCmdCopyBuffer(
        self->instance->command_buffer,
        temp.buffer,
        self->buffer,
        1,
        &copy
    );

    if (self->instance->group) {
        self->instance->group->offset += self->size;
        Py_RETURN_NONE;
    }

    end_commands(self->instance);
    free_temp_buffer(self->instance, &temp);
    Py_RETURN_NONE;
}
