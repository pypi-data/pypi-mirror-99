# Copyright 2020 Q-CTRL Pty Ltd & Q-CTRL Inc. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#     https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

# pylint: disable=too-many-lines
"""Module for unary operation nodes."""

from typing import Union

import forge
import numpy as np

from qctrlcommons.preconditions import (
    check_argument,
    check_argument_numeric,
)

from . import types
from .module import CoreNode
from .node_data import (
    StfNodeData,
    TensorPwcNodeData,
)
from .tensorflow import TensorNodeData
from .utils import (
    validate_shape,
    validate_values_and_batch_shape,
)

NumericOrFunction = Union[
    float, complex, np.ndarray, types.Tensor, types.TensorPwc, types.Stf
]


def _create_flexible_unary_node_data(_operation, x, name, values_shape_changer=None):
    """
    Common implementation of `create_node_data` for nodes acting on Tensors, Pwcs, and Stfs
    implementing unary functions.

    Parameters
    ----------
    _operation : Operation
        The operation to implement.
    x : number or np.ndarray or Tensor or TensorPwc or Stf
        The object on which the operation acts.
    name : str
        The name of the node.
    values_shape_changer : Callable[[tuple], tuple], optional
        Callable that transforms the original shape of the object into the shape after the operation
        is applied. Defaults to an identity operation, that is to say, to not change the shape.

    Returns
    -------
    Tensor or TensorPwc or Stf
        The operation acting on the object.
    """

    # By default don't change shapes.
    if values_shape_changer is None:
        values_shape_changer = lambda shape: shape

    if isinstance(x, StfNodeData):
        check_argument(
            name is None,
            "You can't assign a name to an Stf node.",
            {"name": name},
        )
        values_shape, batch_shape = validate_values_and_batch_shape(x, "x")
        return StfNodeData(
            _operation,
            values_shape=values_shape_changer(values_shape),
            batch_shape=batch_shape,
        )

    if isinstance(x, TensorPwcNodeData):
        values_shape, batch_shape = validate_values_and_batch_shape(x, "x")
        return TensorPwcNodeData(
            _operation,
            values_shape=values_shape_changer(values_shape),
            durations=x.durations,
            batch_shape=batch_shape,
        )

    check_argument_numeric(x, "x")
    shape = validate_shape(x, "x")
    return TensorNodeData(_operation, shape=values_shape_changer(shape))


class Sqrt(CoreNode):
    r"""
    Returns the element-wise square root of an object. This can be a number, an array, a tensor, or
    a time-dependent function in the form of a TensorPwc or an Stf.

    Parameters
    ----------
    x : number or np.ndarray or Tensor or TensorPwc or Stf
        The object whose square root you want to calculate, :math:`x`. For numbers, arrays, and
        tensors, the object is converted to a tensor and then the operation is applied. For
        functions of time (TensorPwcs and Stfs), the composition of the operation with the function
        is computed (that is, the operation is applied to the function values).
    name : str, optional
        The name of the node. You can only provide a name if the object is not an Stf.

    Returns
    -------
    Tensor or TensorPwc or Stf
        The element-wise square root, :math:`\sqrt{x}`, of the values or function you provided.
        The returned object is of the same kind as the one you provided, except if you provide a
        number or an np.ndarray in which case it's a Tensor.
    """

    name = "sqrt"
    _module_attr = "sqrt_operation"
    args = [forge.arg("x", type=NumericOrFunction)]
    rtype = Union[types.Tensor, types.TensorPwc, types.Stf]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        return _create_flexible_unary_node_data(_operation, **kwargs)


class Sin(CoreNode):
    r"""
    Returns the element-wise sine of an object. This can be a number, an array, a tensor, or
    a time-dependent function in the form of a TensorPwc or an Stf.

    Parameters
    ----------
    x : number or np.ndarray or Tensor or TensorPwc or Stf
        The object whose sine you want to calculate, :math:`x`. For numbers, arrays, and
        tensors, the object is converted to a tensor and then the operation is applied. For
        functions of time (TensorPwcs and Stfs), the composition of the operation with the function
        is computed (that is, the operation is applied to the function values).
    name : str, optional
        The name of the node. You can only provide a name if the object is not an Stf.

    Returns
    -------
    Tensor or TensorPwc or Stf
        The element-wise sine, :math:`\sin{x}`, of the values or function you provided.
        The returned object is of the same kind as the one you provided, except if you provide a
        number or an np.ndarray in which case it's a Tensor.
    """

    name = "sin"
    _module_attr = "sin_operation"
    args = [forge.arg("x", type=NumericOrFunction)]
    rtype = Union[types.Tensor, types.TensorPwc, types.Stf]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        return _create_flexible_unary_node_data(_operation, **kwargs)


class Cos(CoreNode):
    r"""
    Returns the element-wise cosine of an object. This can be a number, an array, a tensor, or
    a time-dependent function in the form of a TensorPwc or an Stf.

    Parameters
    ----------
    x : number or np.ndarray or Tensor or TensorPwc or Stf
        The object whose cosine you want to calculate, :math:`x`. For numbers, arrays, and
        tensors, the object is converted to a tensor and then the operation is applied. For
        functions of time (TensorPwcs and Stfs), the composition of the operation with the function
        is computed (that is, the operation is applied to the function values).
    name : str, optional
        The name of the node. You can only provide a name if the object is not an Stf.

    Returns
    -------
    Tensor or TensorPwc or Stf
        The element-wise cosine, :math:`\cos{x}`, of the values or function you provided.
        The returned object is of the same kind as the one you provided, except if you provide a
        number or an np.ndarray in which case it's a Tensor.
    """

    name = "cos"
    _module_attr = "cos_operation"
    args = [forge.arg("x", type=NumericOrFunction)]
    rtype = Union[types.Tensor, types.TensorPwc, types.Stf]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        return _create_flexible_unary_node_data(_operation, **kwargs)


class Tan(CoreNode):
    r"""
    Returns the element-wise tangent of an object. This can be a number, an array, a tensor, or
    a time-dependent function in the form of a TensorPwc or an Stf.

    Parameters
    ----------
    x : number or np.ndarray or Tensor or TensorPwc or Stf
        The object whose tangent you want to calculate, :math:`x`. For numbers, arrays, and
        tensors, the object is converted to a tensor and then the operation is applied. For
        functions of time (TensorPwcs and Stfs), the composition of the operation with the function
        is computed (that is, the operation is applied to the function values).
    name : str, optional
        The name of the node. You can only provide a name if the object is not an Stf.

    Returns
    -------
    Tensor or TensorPwc or Stf
        The element-wise tangent, :math:`\tan{x}`, of the values or function you provided.
        The returned object is of the same kind as the one you provided, except if you provide a
        number or an np.ndarray in which case it's a Tensor.
    """

    name = "tan"
    _module_attr = "tan_operation"
    args = [forge.arg("x", type=NumericOrFunction)]
    rtype = Union[types.Tensor, types.TensorPwc, types.Stf]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        return _create_flexible_unary_node_data(_operation, **kwargs)


class Sinh(CoreNode):
    r"""
    Returns the element-wise hyperbolic sine of an object. This can be a number, an array,
    a tensor, or a time-dependent function in the form of a TensorPwc or an Stf.

    Parameters
    ----------
    x : number or np.ndarray or Tensor or TensorPwc or Stf
        The object whose hyperbolic sine you want to calculate, :math:`x`. For numbers, arrays, and
        tensors, the object is converted to a tensor and then the operation is applied. For
        functions of time (TensorPwcs and Stfs), the composition of the operation with the function
        is computed (that is, the operation is applied to the function values).
    name : str, optional
        The name of the node. You can only provide a name if the object is not an Stf.

    Returns
    -------
    Tensor or TensorPwc or Stf
        The element-wise hyperbolic sine, :math:`\sinh{x}`, of the values or function you provided.
        The returned object is of the same kind as the one you provided, except if you provide a
        number or an np.ndarray in which case it's a Tensor.
    """

    name = "sinh"
    _module_attr = "sinh_operation"
    args = [forge.arg("x", type=NumericOrFunction)]
    rtype = Union[types.Tensor, types.TensorPwc, types.Stf]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        return _create_flexible_unary_node_data(_operation, **kwargs)


class Cosh(CoreNode):
    r"""
    Returns the element-wise hyperbolic cosine of an object. This can be a number, an array,
    a tensor, or a time-dependent function in the form of a TensorPwc or an Stf.

    Parameters
    ----------
    x : number or np.ndarray or Tensor or TensorPwc or Stf
        The object whose hyperbolic cosine you want to calculate, :math:`x`. For numbers, arrays,
        and tensors, the object is converted to a tensor and then the operation is applied. For
        functions of time (TensorPwcs and Stfs), the composition of the operation with the function
        is computed (that is, the operation is applied to the function values).
    name : str, optional
        The name of the node. You can only provide a name if the object is not an Stf.

    Returns
    -------
    Tensor or TensorPwc or Stf
        The element-wise hyperbolic cosine, :math:`\cosh{x}`, of the values or function you
        provided. The returned object is of the same kind as the one you provided, except if you
        provide a number or an np.ndarray in which case it's a Tensor.
    """

    name = "cosh"
    _module_attr = "cosh_operation"
    args = [forge.arg("x", type=NumericOrFunction)]
    rtype = Union[types.Tensor, types.TensorPwc, types.Stf]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        return _create_flexible_unary_node_data(_operation, **kwargs)


class Tanh(CoreNode):
    r"""
    Returns the element-wise hyperbolic tangent of an object. This can be a number, an array,
    a tensor, or a time-dependent function in the form of a TensorPwc or an Stf.

    Parameters
    ----------
    x : number or np.ndarray or Tensor or TensorPwc or Stf
        The object whose hyperbolic tangent you want to calculate, :math:`x`. For numbers, arrays,
        and tensors, the object is converted to a tensor and then the operation is applied. For
        functions of time (TensorPwcs and Stfs), the composition of the operation with the function
        is computed (that is, the operation is applied to the function values).
    name : str, optional
        The name of the node. You can only provide a name if the object is not an Stf.

    Returns
    -------
    Tensor or TensorPwc or Stf
        The element-wise hyperbolic tangent, :math:`\tanh{x}`, of the values or function you
        provided. The returned object is of the same kind as the one you provided, except if you
        provide a number or an np.ndarray in which case it's a Tensor.
    """

    name = "tanh"
    _module_attr = "tanh_operation"
    args = [forge.arg("x", type=NumericOrFunction)]
    rtype = Union[types.Tensor, types.TensorPwc, types.Stf]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        return _create_flexible_unary_node_data(_operation, **kwargs)


class Arcsin(CoreNode):
    r"""
    Returns the element-wise arcsine of an object. This can be a number, an array,
    a tensor, or a time-dependent function in the form of a TensorPwc or an Stf.

    Parameters
    ----------
    x : float or np.ndarray or Tensor or TensorPwc or Stf
        The object whose arcsine you want to calculate, :math:`x`. Must be real. For numbers,
        arrays, and tensors, the object is converted to a tensor and then the operation is applied.
        For functions of time (TensorPwcs and Stfs), the composition of the operation with the
        function is computed (that is, the operation is applied to the function values).
    name : str, optional
        The name of the node. You can only provide a name if the object is not an Stf.

    Returns
    -------
    Tensor or TensorPwc or Stf
        The element-wise arcsine, :math:`\arcsin{x}`, of the values or function you
        provided. Outputs will be in the range of :math:`[-\pi/2, \pi/2]`.
        The returned object is of the same kind as the one you provided, except if you
        provide a number or an np.ndarray in which case it's a Tensor.
    """

    name = "arcsin"
    _module_attr = "arcsin_operation"
    args = [forge.arg("x", type=NumericOrFunction)]
    rtype = Union[types.Tensor, types.TensorPwc, types.Stf]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        return _create_flexible_unary_node_data(_operation, **kwargs)


class Arccos(CoreNode):
    r"""
    Returns the element-wise arccosine of an object. This can be a number, an array,
    a tensor, or a time-dependent function in the form of a TensorPwc or an Stf.

    Parameters
    ----------
    x : float or np.ndarray or Tensor or TensorPwc or Stf
        The object whose arccosine you want to calculate, :math:`x`. Must be real. For numbers,
        arrays, and tensors, the object is converted to a tensor and then the operation is applied.
        For functions of time (TensorPwcs and Stfs), the composition of the operation with the
        function is computed (that is, the operation is applied to the function values).
    name : str, optional
        The name of the node. You can only provide a name if the object is not an Stf.

    Returns
    -------
    Tensor or TensorPwc or Stf
        The element-wise arccosine, :math:`\arccos{x}`, of the values or function you
        provided. Outputs will be in the range of :math:`[0, \pi]`.
        The returned object is of the same kind as the one you provided, except if you
        provide a number or an np.ndarray in which case it's a Tensor.
    """

    name = "arccos"
    _module_attr = "arccos_operation"
    args = [forge.arg("x", type=NumericOrFunction)]
    rtype = Union[types.Tensor, types.TensorPwc, types.Stf]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        return _create_flexible_unary_node_data(_operation, **kwargs)


class Arctan(CoreNode):
    r"""
    Returns the element-wise arctangent of an object. This can be a number, an array,
    a tensor, or a time-dependent function in the form of a TensorPwc or an Stf.

    Parameters
    ----------
    x : float or np.ndarray or Tensor or TensorPwc or Stf
        The object whose arctangent you want to calculate, :math:`x`. Must be real. For numbers,
        arrays, and tensors, the object is converted to a tensor and then the operation is applied.
        For functions of time (TensorPwcs and Stfs), the composition of the operation with the
        function is computed (that is, the operation is applied to the function values).
    name : str, optional
        The name of the node. You can only provide a name if the object is not an Stf.

    Returns
    -------
    Tensor or TensorPwc or Stf
        The element-wise arctangent, :math:`\arctan{x}`, of the values or function you
        provided. Outputs will be in the range of :math:`[-\pi/2, \pi/2]`.
        The returned object is of the same kind as the one you provided, except if you
        provide a number or an np.ndarray in which case it's a Tensor.
    """

    name = "arctan"
    _module_attr = "arctan_operation"
    args = [forge.arg("x", type=NumericOrFunction)]
    rtype = Union[types.Tensor, types.TensorPwc, types.Stf]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        return _create_flexible_unary_node_data(_operation, **kwargs)
