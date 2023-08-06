"""
Test shap decomposition calculations
"""
import logging
from typing import Set, Tuple, Union

import numpy as np
import pandas as pd
import pytest

from pytools.viz.dendrogram import LinkageTree
from sklearndf.pipeline import RegressorPipelineDF

from facet.crossfit import LearnerCrossfit
from facet.inspection import LearnerInspector

log = logging.getLogger(__name__)


def test_shap_decomposition(regressor_inspector: LearnerInspector) -> None:

    # noinspection PyPep8Naming
    def _calculate_relative_syn_and_red(
        feature_x: str, feature_y: str, is_indirect_syn_valid: bool
    ) -> Tuple[float, float, float, float]:
        iv = regressor_inspector.shap_interaction_values(consolidate=None)
        # Get 3 components for each feature:
        # S = interaction SHAP
        # A, B = independent SHAP
        # U, V = sum of interactions with 3rd variables
        iv_x = iv.xs(feature_x, level=-1)
        iv_y = iv.xs(feature_y, level=-1)
        X = iv_x.sum(axis=1).rename("X")
        Y = iv_y.sum(axis=1).rename("Y")
        A = iv_x.loc[:, feature_x]
        B = iv_y.loc[:, feature_y]
        S = iv_x.loc[:, feature_y]
        U = X - A - S
        V = Y - B - S
        # calculate the "indirect" S, such that cov(U, S) == 0 and cov(V, S) == 0
        k_U = max(0.0, cov(S, U) / var(S)) if is_indirect_syn_valid else 0.0
        k_V = max(0.0, cov(S, V) / var(S)) if is_indirect_syn_valid else 0.0
        print_list(**{"cov(U, S) / var(S)": k_U, "cov(V, S) / var(S)": k_V})
        varS = var(S)
        Su = S if varS == 0 else S * k_U
        Sv = S if varS == 0 else S * k_V
        U_ = U - Su
        V_ = V - Sv
        print_list(
            stdS=std(S),
            stdSu=std(Su),
            stdSv=std(Sv),
            stdU=std(U),
            stdU_=std(U_),
            stdV=std(V),
            stdV_=std(V_),
        )
        # calculate the minimal shared vector R, such that cov(X_ - R, Y_ - R) == 0
        X_ = X - S - Su
        Y_ = Y - S - Sv
        AUT = X_ + Y_
        AUT_asym = X_
        R_ = AUT / 2
        dXY = std(X_ - Y_)
        dR = std(R_)
        R = R_ * (1 - dXY / (2 * dR))
        print_list(
            stdX=std(X),
            stdY=std(Y),
            stdX_=std(X_),
            stdY_=std(Y_),
            stdR=std(R),
            covX_R_Y_R=round(cov(X_ - R, Y_ - R), 15),
        )
        SYN = 2 * S + Su + Sv
        SYN_asym = S + Su
        RED = 2 * R
        RED_asym = R
        UNI = X + Y - RED
        UNI_asym = X - RED_asym
        syn = std(SYN)
        aut = std(AUT)
        red = std(RED)
        uni = std(UNI)
        syn_asym = std(SYN_asym)
        aut_asym = std(AUT_asym)
        red_asym = std(RED_asym)
        uni_asym = std(UNI_asym)
        print_list(syn=syn, aut=aut, red=red, uni=uni)
        return (
            syn / (syn + aut),
            red / (red + uni),
            syn_asym / (syn_asym + aut_asym),
            red_asym / (red_asym + uni_asym),
        )

    for i, j, indirect_syn in [
        ("LSTAT", "RM", False),
        ("LSTAT", "DIS", True),
        ("LSTAT", "AGE", False),
        ("LSTAT", "NOX", False),
        ("LSTAT", "CRIM", False),
        ("RM", "DIS", False),
        ("RM", "AGE", False),
        ("RM", "NOX", False),
        ("RM", "CRIM", False),
    ]:
        print(f"\ncomparing features X={i} and Y={j}")

        syn_rel, red_rel, syn_rel_asym, red_rel_asym = _calculate_relative_syn_and_red(
            feature_x=i, feature_y=j, is_indirect_syn_valid=indirect_syn
        )

        syn_matrix = regressor_inspector.feature_synergy_matrix(symmetrical=True)
        red_matrix = regressor_inspector.feature_redundancy_matrix(symmetrical=True)
        syn_matrix_asym = regressor_inspector.feature_synergy_matrix()
        red_matrix_asym = regressor_inspector.feature_redundancy_matrix()

        print_list(
            syn_rel=syn_rel,
            red_rel=red_rel,
            syn_rel_asym=syn_rel_asym,
            red_rel_asym=red_rel_asym,
            syn_matrix=syn_matrix.loc[i, j],
            red_matrix=red_matrix.loc[i, j],
            syn_matrix_asym=syn_matrix_asym.loc[i, j],
            red_matrix_asym=red_matrix_asym.loc[i, j],
            percentage=True,
        )

        assert np.isclose(red_matrix.loc[i, j], red_rel)
        assert np.isclose(red_matrix.loc[j, i], red_rel)
        assert np.isclose(syn_matrix.loc[i, j], syn_rel)
        assert np.isclose(syn_matrix.loc[j, i], syn_rel)
        assert np.isclose(red_matrix_asym.loc[i, j], red_rel_asym)
        assert np.isclose(syn_matrix_asym.loc[i, j], syn_rel_asym)

        # check basic matrix properties

        n_features = len(regressor_inspector.features)

        for matrix in (syn_matrix, syn_matrix_asym, red_matrix, red_matrix_asym):
            # matrix shape is n_features x n_features
            assert matrix.shape == (n_features, n_features)

            # values on the diagonal are all 1.0
            for a in range(n_features):
                assert matrix.iloc[a, a] == 1.0

            # there are no nan values
            assert matrix.notna().all().all()


def test_shap_decomposition_matrices(
    best_lgbm_crossfit: LearnerCrossfit[RegressorPipelineDF],
    feature_names: Set[str],
    regressor_inspector: LearnerInspector,
) -> None:
    # Shap decomposition matrices (feature dependencies)
    association_matrix: pd.DataFrame = regressor_inspector.feature_association_matrix(
        clustered=False, symmetrical=True
    )

    # check that dimensions of pairwise feature matrices are equal to # of features,
    # and value ranges:
    for matrix, matrix_name in zip(
        (
            association_matrix,
            regressor_inspector.feature_synergy_matrix(),
            regressor_inspector.feature_redundancy_matrix(),
        ),
        ("association", "synergy", "redundancy"),
    ):
        matrix_full_name = f"feature {matrix_name} matrix"
        n_features = len(feature_names)
        assert len(matrix) == n_features, f"rows in {matrix_full_name}"
        assert len(matrix.columns) == n_features, f"columns in {matrix_full_name}"

        # check values
        for c in matrix.columns:
            assert (
                0.0
                <= matrix.fillna(0).loc[:, c].min()
                <= matrix.fillna(0).loc[:, c].max()
                <= 1.0
            ), f"Values of [0.0, 1.0] in {matrix_full_name}"

    # check actual values:
    assert association_matrix.values == pytest.approx(
        np.array(
            [
                [1.0, 0.043, 0.233, 0.0, 0.162, 0.078]
                + [0.192, 0.156, 0.009, 0.022, 0.035, 0.008, 0.07],
                [0.043, 1.0, 0.155, 0.0, 0.056, 0.055]
                + [0.017, 0.225, 0.024, 0.021, 0.049, 0.145, 0.034],
                [0.233, 0.155, 1.0, 0.0, 0.123, 0.207]
                + [0.15, 0.044, 0.069, 0.225, 0.241, 0.149, 0.209],
                [0.0, 0.0, 0.0, 1.0, 0.0, 0.0] + [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.162, 0.056, 0.123, 0.0, 1.0, 0.051]
                + [0.017, 0.156, 0.19, 0.08, 0.15, 0.025, 0.029],
                [0.078, 0.055, 0.207, 0.0, 0.051, 1.0]
                + [0.088, 0.005, 0.081, 0.14, 0.027, 0.058, 0.49],
                [0.192, 0.017, 0.15, 0.0, 0.017, 0.088]
                + [1.0, 0.128, 0.015, 0.269, 0.14, 0.096, 0.295],
                [0.156, 0.225, 0.044, 0.0, 0.156, 0.005]
                + [0.128, 1.0, 0.255, 0.158, 0.273, 0.132, 0.023],
                [0.009, 0.024, 0.069, 0.0, 0.19, 0.081]
                + [0.015, 0.255, 1.0, 0.223, 0.188, 0.035, 0.049],
                [0.022, 0.021, 0.225, 0.0, 0.08, 0.14]
                + [0.269, 0.158, 0.223, 1.0, 0.284, 0.182, 0.097],
                [0.035, 0.049, 0.241, 0.0, 0.15, 0.027]
                + [0.14, 0.273, 0.188, 0.284, 1.0, 0.027, 0.031],
                [0.008, 0.145, 0.149, 0.0, 0.025, 0.058]
                + [0.096, 0.132, 0.035, 0.182, 0.027, 1.0, 0.057],
                [0.07, 0.034, 0.209, 0.0, 0.029, 0.49]
                + [0.295, 0.023, 0.049, 0.097, 0.031, 0.057, 1.0],
            ]
        ),
        abs=0.02,
    )

    # cluster associated features
    association_linkage = regressor_inspector.feature_association_linkage()

    assert isinstance(association_linkage, LinkageTree)


#
# auxiliary functions
#


def cov(a: np.ndarray, b: np.ndarray) -> float:
    """
    covariance, assuming a population mean of 0
    :param a: array of floats
    :param b: array of floats
    :return: covariance of a and b
    """
    return (a * b).mean()


def var(a: np.ndarray) -> float:
    """
    variance, assuming a population mean of 0
    :param a: array of floats
    :return: variance of a
    """
    return cov(a, a)


def std(a: np.ndarray) -> float:
    """
    standard deviation, assuming a population mean of 0
    :param a: array of floats
    :return: standard deviation of a
    """
    return np.sqrt(var(a))


def corr(a: np.ndarray, b: np.ndarray) -> float:
    """
    pearson correlation, assuming a population mean of 0
    :param a: array of floats
    :param b: array of floats
    :return: pearson correlation of a and b
    """
    return cov(a, b) / np.sqrt(var(a) * var(b))


def print_list(*args, percentage: bool = False, **kwargs):
    """
    print all arguments, including their names
    :param args: the arguments to print (as their names, print integers indicating \
        the position)
    :param percentage: if `true`, print all arguments as % values
    :param kwargs: the named arguments to print
    :return:
    """

    def _prt(_value, _name: Union[str, int]):
        if percentage:
            _value *= 100
        print(f"{_name}: {_value:.4g}{'%' if percentage else ''}")

    for name, arg in enumerate(args):
        _prt(arg, _name=name)
    for name, arg in kwargs.items():
        _prt(arg, _name=name)
