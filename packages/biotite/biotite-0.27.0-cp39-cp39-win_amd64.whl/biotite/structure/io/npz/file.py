# This source code is part of the Biotite package and is distributed
# under the 3-Clause BSD License. Please see 'LICENSE.rst' for further
# information.

__name__ = "biotite.structure.io.npz"
__author__ = "Patrick Kunzmann"
__all__ = ["NpzFile"]

import numpy as np
from ...atoms import Atom, AtomArray, AtomArrayStack
from ...bonds import BondList
from ....file import File, is_binary


class NpzFile(File):
    r"""
    This class represents a NPZ file, the preferable format for
    Biotite internal structure storage. 
    
    Internally the this class writes/reads all attribute arrays of an
    :class:`AtomArray` or :class:`AtomArrayStack` using the *NumPy*
    :func:`save()`/:func:`load()`
    method. This format offers the fastest I/O operations and completely
    preserves the content all atom annotation arrays.
    
    Examples
    --------
    Load a \\*.npz file, modify the structure and save the new
    structure into a new file:
    
    >>> import os.path
    >>> file = NpzFile.read(os.path.join(path_to_structures, "1l2y.npz"))
    >>> array_stack = file.get_structure()
    >>> array_stack_mod = rotate(array_stack, [1,2,3])
    >>> file = NpzFile()
    >>> file.set_structure(array_stack_mod)
    >>> file.write(os.path.join(path_to_directory, "1l2y_mod.npz"))
    
    """
    
    def __init__(self):
        super().__init__()
        self._data_dict = None
    
    def __copy_fill__(self, clone):
        super().__copy_fill__(clone)
        if self._data_dict is not None:
            for key, value in self._data_dict.items():
                clone._data_dict[key] = np.copy(value)
    
    @classmethod
    def read(cls, file):
        """
        Read a NPZ file.
        
        Parameters
        ----------
        file : file-like object or str
            The file to be read.
            Alternatively a file path can be supplied.
        
        Returns
        -------
        file_object : NPZFile
            The parsed file.
        """
        npz_file = NpzFile()
        # File name
        if isinstance(file, str):
            with open(file, "rb") as f:
                npz_file._data_dict = dict(np.load(f, allow_pickle=False))
        # File object
        else:
            if not is_binary(file):
                raise TypeError("A file opened in 'binary' mode is required")
            npz_file._data_dict = dict(np.load(file, allow_pickle=False))
        return npz_file
                
    def write(self, file):
        """
        Write a NPZ file.
        
        Parameters
        ----------
        file : file-like object or str
            The file to be read.
            Alternatively, a file path can be supplied.
        """
        if isinstance(file, str):
            with open(file, "wb") as f:
                np.savez(f, **self._data_dict)
        else:
            if not is_binary(file):
                raise TypeError("A file opened in 'binary' mode is required")
            np.savez(file, **self._data_dict)
    
    def get_structure(self):
        """
        Get an :class:`AtomArray` or :class:`AtomArrayStack` from the
        file.
        
        If this method returns an array or stack depends on which type
        of object was used when the file was written.
        
        Returns
        -------
        array : AtomArray or AtomArrayStack
            The array or stack contained in this file.
        """
        if self._data_dict is None:
            raise ValueError("The structure of this file "
                             "has not been loaded or set yet")
        coord = self._data_dict["coord"]
        # The type of the structure is determined by the dimensionality
        # of the 'coord' field
        if len(coord.shape) == 3:
            array = AtomArrayStack(coord.shape[0], coord.shape[1])
        else:
            array = AtomArray(coord.shape[0])
        
        for key, value in self._data_dict.items():
            if key == "coord":
                array.coord = value
            elif key == "bonds":
                array.bonds = BondList(array.array_length(), value)
            elif key == "box":
                array.box = value
            else:
                array.set_annotation(key, value)
        return array
        
    def set_structure(self, array):
        """
        Set the :class:`AtomArray` or :class:`AtomArrayStack` for the
        file.
        
        Parameters
        ----------
        array : AtomArray or AtomArrayStack
            The array or stack to be saved into this file.
        """
        self._data_dict = {}
        self._data_dict["coord"] = np.copy(array.coord)
        if array.bonds is not None:
            self._data_dict["bonds"] = array.bonds.as_array()
        if array.box is not None:
            self._data_dict["box"] = np.copy(array.box)
        for annot in array.get_annotation_categories():
            self._data_dict[annot] = np.copy(array.get_annotation(annot))