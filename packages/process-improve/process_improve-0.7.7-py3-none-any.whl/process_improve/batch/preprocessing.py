from typing import Dict, List
import numpy as np
import pandas as pd
import logging
import plotly.graph_objects as go

from .alignment_helpers import distance_matrix, backtrack_optimal_path

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(f"{__file__}.log")
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

# dtwalign: https://github.com/statefb/dtwalign
# from dtwalign import dtw_from_distance_matrix

epsqrt = np.sqrt(np.finfo(float).eps)


def determine_scaling(
    batches: Dict[str, pd.DataFrame],
    columns_to_align: List = None,
    settings: dict = None,
) -> pd.DataFrame:
    """
    Scales the batch data according to the variable ranges.

    Parameters
    ----------
    dict_df : Dict[str, pd.DataFrame]
        Batch data, in the standard format.

    Returns
    -------
    range_scalers: DataFrame

        J rows
        2 columns:
            column 1 = Range of each tag. Approximated as the typical delta from q98 - q02
            column 2 = Typical minimum of each tag. Robustly calculated.

    TODO: put this in a scikit-learn style: .fit() and .apply() style
    """
    # This will be clumsy, until we have Python 3.9
    default_settings = {"robust": True}
    if settings:
        default_settings.update(settings)

    settings = default_settings
    if columns_to_align is None:
        columns_to_align = batches[list(batches.keys())[0]].columns

    collector_rnge = []
    collector_mins = []
    for _, batch in batches.items():
        if settings["robust"]:
            rnge = batch[columns_to_align].quantile(0.98) - batch[
                columns_to_align
            ].quantile(0.02)
        else:
            rnge = batch[columns_to_align].max() - batch[columns_to_align].min()

        rnge[rnge.values == 0] = 1.0
        collector_rnge.append(rnge)
        collector_mins.append(batch.min())

    if settings["robust"]:
        scalings = pd.concat(
            [
                pd.DataFrame(collector_rnge).median(),
                pd.DataFrame(collector_mins).median(),
            ],
            axis=1,
        )
    else:
        scalings = pd.concat(
            [pd.DataFrame(collector_rnge).mean(), pd.DataFrame(collector_mins).mean()],
            axis=1,
        )
    scalings.columns = ["Range", "Minimum"]
    scalings["Minimum"] = 0.0
    return scalings


def apply_scaling(
    batches: Dict[str, pd.DataFrame],
    scale_df: pd.DataFrame,
    columns_to_align: List = None,
) -> dict:
    """Scales the batches according to the information in the scaling dataframe.

    Parameters
    ----------
    batches : Dict[str, pd.DataFrame]
        The batches, in standard format.
    scale_df : pd.DataFrame
        The scaling dataframe, from `determine_scaling`

    Returns
    -------
    dict
        The scaled batch data.
    """
    # TODO: handle the case of DataFrames still
    if columns_to_align is None:
        if isinstance(batches, dict):
            batch1 = batches[list(batches.keys())[0]]
            columns_to_align = batch1.columns
        else:
            columns_to_align = batches.columns
    out = {}
    for batch_id, batch in batches.items():
        out[batch_id] = batch[columns_to_align].copy()
        for tag, column in out[batch_id].iteritems():
            out[batch_id][tag] = (column - scale_df.loc[tag, "Minimum"]) / scale_df.loc[
                tag, "Range"
            ]
    return out


def reverse_scaling(
    batches: Dict[str, pd.DataFrame],
    scale_df: pd.DataFrame,
    columns_to_align: List = None,
):
    # TODO: handle the case of DataFrames still
    if columns_to_align is None:
        if isinstance(batches, dict):
            columns_to_align = batches[list(batches.keys())[0]].columns
        else:
            columns_to_align = batches.columns
    out = {}
    for batch_id, batch in batches.items():
        out[batch_id] = batch[columns_to_align].copy()
        for tag, column in out[batch_id].iteritems():
            out[batch_id][tag] = (
                column * scale_df.loc[tag, "Range"] + scale_df.loc[tag, "Minimum"]
            )
    return out


class DTWresult:
    """Result class."""

    def __init__(
        self,
        synced: np.ndarray,
        penalty_matrix: np.ndarray,
        md_path: np.ndarray,  # multi-dimensional path through distance mesh D = penalty_matrix
        warping_path: np.ndarray,
        distance: float,
        normalized_distance: float,
    ):
        self.synced = synced
        self.penalty_matrix = penalty_matrix
        self.md_path = md_path
        self.warping_path = warping_path
        self.distance = distance
        self.normalized_distance = normalized_distance


def align_with_path(md_path, batch, initial_row):
    row = 0
    nr = md_path[:, 0].max() + 1  # to account for the zero-based indexing
    synced = np.zeros((nr, batch.shape[1]))
    synced[row, :] = batch.iloc[md_path[0, 1], :]
    temp = initial_row
    for idx in np.arange(1, md_path.shape[0]):
        if md_path[idx, 0] != md_path[idx - 1, 0]:
            row += 1
            synced[row, :] = temp = batch.iloc[md_path[idx, 1], :]

        else:
            # TODO : Come back to page 181 of thesis: where more than 1 point in the target
            #        trajectory is aligned with the reference: compute the average,
            temp = np.vstack((temp, batch.iloc[md_path[idx, 1], :]))
            synced[row, :] = np.nanmean(temp, axis=0)

    return pd.DataFrame(synced, columns=batch.columns)


def dtw_core(test, ref, weight_matrix: np.ndarray):

    show_plot = False
    nt = test.shape[0]  # 'test' data; will be align to the 'reference' data
    nr = ref.shape[0]
    assert test.shape[1] == ref.shape[1]

    D = distance_matrix(test.values, ref.values, weight_matrix)
    md_path, distance = backtrack_optimal_path(D)
    warping_path = np.zeros(nr)
    for idx in range(nr):
        warping_path[idx] = md_path[np.where(md_path[:, 0] == idx)[0][-1], 1]

    # Now align the `test` batch:
    initial_row = ref.iloc[md_path[0, 0], :].copy()
    synced = align_with_path(md_path=md_path, batch=test, initial_row=initial_row)

    if show_plot:  # for debugging
        X = np.arange(0, nt, 1)
        Y = np.arange(0, nr, 1)
        X, Y = np.meshgrid(X, Y)
        fig = go.Figure(
            data=[
                go.Mesh3d(
                    x=X.ravel(),
                    y=Y.ravel(),
                    z=D.ravel(),
                    color="lightpink",
                    opacity=0.90,
                )
            ]
        )
        fig.show()

    return DTWresult(
        synced,
        D,
        md_path,
        warping_path,
        distance,
        normalized_distance=distance / (nr + nt),
    )


def one_iteration_dtw(
    batches_scaled: dict,
    refbatch_sc: pd.DataFrame,
    weight_matrix: np.ndarray,
    settings: dict = None,
):
    default_settings = {"show_progress": True, "subsample": 1}
    if settings:
        default_settings.update(settings)
    settings = default_settings

    aligned_batches = {}
    distances = []
    average_batch = refbatch_sc.copy().reset_index(drop=True) * 0.0
    successful_alignments = 0
    for batch_id, batch in batches_scaled.items():
        try:
            # see Kassidas, page 180
            batch_subset = batch.iloc[:: settings["subsample"], :]
            result = dtw_core(batch_subset, refbatch_sc, weight_matrix=weight_matrix)
            average_batch += result.synced
            aligned_batches[batch_id] = result
            successful_alignments += 1
            distances.append(
                {
                    "batch_id": batch_id,
                    "Distance": result.distance,
                    "Normalized distance": result.normalized_distance,
                }
            )
            if settings["show_progress"]:
                message = f"  * {batch_id}: distance = {result.distance}"
                logger.debug(message)
                print(message)
        except ValueError:
            assert False, f"Failed on batch {batch_id}"

    average_batch /= successful_alignments

    return aligned_batches, average_batch


def batch_dtw(
    batches: Dict[str, pd.DataFrame],
    columns_to_align: list,
    reference_batch: str,
    settings: dict = None,
) -> dict:
    """
    Synchronize, via iterative DTW, with weighting.

    Algorithm: Kassidas et al. (2004):  https://doi.org/10.1002/aic.690440412

    Parameters
    ----------
    batches : Dict[str, pd.DataFrame]
        Batch data, in the standard format.
    columns_to_align : list
        Which columns to use during the alignment process. The others are aligned, but
        get no weight, and therefore do not influence the objective function.
    reference_batch : str
        Which key in the `batches` is the reference batch.
    maximum_iterations : int
        The maximum number of iterations allowed.

    Returns
    -------
    dict
        Various outputs relevant to the alignment.
        TODO: Document completely later.

    Notation
    --------
    I = number of batches: index = i
    i = index for the batches
    J = number of tags (columns in each batch)
    j = index for the tags
    k = index into the rows of each batch, the samples: 0 ... k ... K_i
    """
    default_settings = {
        "maximum_iterations": 25,  # maximum iterations (stops here, even if not converged)
        "tolerance": 0.1,  # convergence tolerance
        "robust": True,  # use robust scaling
        "show_progress": True,  # show progress
        "subsample": 1,  # use every sample
    }
    if settings:
        default_settings.update(settings)
    settings = default_settings
    assert settings["maximum_iterations"] >= 3, "At least 3 iterations are required"
    assert (
        reference_batch in batches
    ), "`reference_batch` was not found in the dict of batches."
    settings["subsample"] = int(settings["subsample"])

    # Checks on the batch data (put in a sub-function)
    for batch_id, batch in batches.items():
        if "batch_id" not in batch.columns:
            batches[batch_id].insert(0, "batch_id", batch_id)

    scale_df = determine_scaling(
        batches=batches, columns_to_align=columns_to_align, settings=settings
    )
    batches_scaled = apply_scaling(batches, scale_df, columns_to_align)
    refbatch_sc = batches_scaled[reference_batch].iloc[:: int(settings["subsample"]), :]
    weight_vector = np.ones(refbatch_sc.shape[1])
    weight_matrix = np.diag(weight_vector)
    weight_history = np.zeros_like(weight_vector) * np.nan

    delta_weight = np.linalg.norm(weight_vector)
    iter = 0
    while (np.linalg.norm(delta_weight) > settings["tolerance"]) and (
        iter <= settings["maximum_iterations"]
    ):
        if settings["show_progress"]:
            message = f"Iter = {iter} and norm = {np.linalg.norm(delta_weight)}"
            logger.debug(message)
            print(message)

        iter += 1
        weight_matrix = np.diag(weight_vector)
        weight_history = np.vstack((weight_history, weight_vector.copy()))

        aligned_batches, average_batch = one_iteration_dtw(
            batches_scaled=batches_scaled,
            refbatch_sc=refbatch_sc,
            weight_matrix=weight_matrix,
            settings=settings,
        )

        # Deviations from the average batch:
        next_weights = np.zeros((1, refbatch_sc.shape[1]))
        for _, result in aligned_batches.items():
            next_weights += np.nansum(
                np.power(result.synced - average_batch, 2), axis=0
            )
            # TODO: use quadratic weights for now, but try sum of the absolute values instead
            #  np.abs(result.synced - average_batch).sum(axis=0)

            # TODO: leave out worst batches when computing the weights
            # dist_df = pd.DataFrame(distances).set_index("batch_id")
            # dist_df.hist("Distance", bins=50)
            # Now find the average trajectory, but ignore problematic batches:
            #      for example, top 5% of the distances.
            # TODO: make this a configurable setting
            # problematic_threshold = dist_df["Distance"].quantile(0.95)

        next_weights = 1.0 / np.where(next_weights > epsqrt, next_weights, 10000)
        weight_vector = (
            next_weights / np.sum(next_weights) * len(columns_to_align)
        ).ravel()
        # If change in delta_weight is small, we terminate early; no need to fine-tune excessively.
        delta_weight = np.diag(weight_matrix) - weight_vector  # old - new

    # OK, the weights are found: now use the last iteration's result to get back to original
    # scaling for the trajectories
    weight_history = weight_history[1:, :]
    aligned_df = pd.DataFrame()
    for batch_id, result in aligned_batches.items():
        initial_row = batches[batch_id].iloc[result.md_path[0, 0], :].copy()
        synced = align_with_path(
            result.md_path,
            batches[batch_id].iloc[:: int(settings["subsample"]), :],
            initial_row=initial_row,
        )
        synced.insert(1, "sequence", list(range(synced.shape[0])))
        aligned_df = aligned_df.append(synced)

    max_places = int(np.ceil(np.log10(aligned_df["sequence"].max())))
    aligned_wide_df = aligned_df.pivot(index="batch_id", columns="sequence")
    new_labels = [
        "-".join(item)
        for item in zip(
            aligned_wide_df.columns.get_level_values(0),
            [
                str(val).zfill(max_places)
                for val in aligned_wide_df.columns.get_level_values(1)
            ],
        )
    ]
    aligned_wide_df.columns = new_labels
    last_average_batch = reverse_scaling(dict(avg=average_batch), scale_df)["avg"]

    return dict(
        scale_df=scale_df,
        aligned_batch_objects=aligned_batches,
        last_average_batch=last_average_batch,
        weight_history=weight_history,
        aligned_wide_df=aligned_wide_df,
    )
