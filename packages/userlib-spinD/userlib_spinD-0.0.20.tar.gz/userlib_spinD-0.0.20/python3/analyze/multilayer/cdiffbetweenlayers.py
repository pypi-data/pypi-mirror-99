# -*- coding: utf-8 -*-
r"""
Module for classes analyzing the differences between properties of the magnetizations of the different layers of a
multilayer system.
"""
from pathlib import Path
from typing import TypeVar, Union
import pandas as pd
import numpy as np

PathLike = TypeVar("PathLike", str, Path)


class CMagDiffCubicLayers:
    r"""
    this class is responsible for calculating the differences between two cubic stacked layers. This can be used to
    measure how simultaneous a collapse might be.
    """

    def __init__(self, allspinfiles: bool = True, spinfileslocation: PathLike = Path.cwd(),
                 specificfile: PathLike = 'spin_0001.dat') -> None:
        r"""
        initializes the calculation of the magnetization deviations in both layers.

        Args:
            allspinfiles(bool): Flag whether all spin_xxx.dat files shell be read and analyzed. The default is True. In this
            case the input parameter vtfileslocation determines where the files should be.

            spinfileslocation(PathLike): All the spin files. Default path is current working directory

            specificfile(PathLike): Only necessary if allspinfiles is False. Then a specific spin-file is analyzed. The
            default is spin_0001.dat here.
        """
        self._allspinfiles = allspinfiles
        self._spinfileslocation = spinfileslocation
        self._specificfile = specificfile

    def __call__(self) -> Union[float, np.ndarray]:
        r"""
        Calls the calculation

        Returns:
            either a float representing the difference of a configuration of a specific file or a 2d numpy array with
            the following structure [[step1, diff1],[step2,diff2],...]
        """
        if self._allspinfiles:
            l_diff, stepindices = [], []
            l_files = Path(self._spinfileslocation).glob('*.dat')
            for f in l_files:
                if str(f).startswith('spin_'):
                    stepindices.append(int(str(f)[5:-4]))
                    df = pd.read_csv(f, sep=r"\s+", index_col=False, usecols=[0, 1, 2, 3, 4, 5],
                                     names=['x', 'y', 'z', 'sx', 'sy', 'sz'])
                    l_df_lower = df['z'] == 0.0
                    l_df_upper = df['z'] != 0.0
                    diffx = l_df_lower['sx'].to_numpy() - l_df_upper['sx'].to_numpy()
                    diffy = l_df_lower['sy'].to_numpy() - l_df_upper['sy'].to_numpy()
                    diffz = l_df_lower['sz'].to_numpy() - l_df_upper['sz'].to_numpy()
                    vec_diff = np.column_stack((diffx, diffy, diffz))
                    l_diff.append(np.sum(np.linalg.norm(vec_diff, axis=1)))
            l_diff = np.asarray(l_diff)
            l_steps = np.asarray(stepindices)
            return np.column_stack((l_steps, l_diff))
        else:
            df = pd.read_csv(self._specificfile, sep=r"\s+", index_col=False, usecols=[0, 1, 2, 3, 4, 5],
                             names=['x', 'y', 'z', 'sx', 'sy', 'sz'])
            l_df_lower = df['z'] == 0.0
            l_df_upper = df['z'] != 0.0
            diffx = l_df_lower['sx'].to_numpy() - l_df_upper['sx'].to_numpy()
            diffy = l_df_lower['sy'].to_numpy() - l_df_upper['sy'].to_numpy()
            diffz = l_df_lower['sz'].to_numpy() - l_df_upper['sz'].to_numpy()
            vec_diff = np.column_stack((diffx, diffy, diffz))
            return np.sum(np.linalg.norm(vec_diff, axis=1))
