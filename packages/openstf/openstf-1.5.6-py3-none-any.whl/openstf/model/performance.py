# SPDX-FileCopyrightText: 2017-2021 Alliander N.V. <korte.termijn.prognoses@alliander.com> # noqa E501>
#
# SPDX-License-Identifier: MPL-2.0

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from ktpbase.database import DataBase
from ktpbase.log import logging

from openstf.feature_engineering.general import calc_completeness
from openstf.model import metrics


def calc_kpi_for_specific_pid(pid, start_time=None, end_time=None):
    """Function that checks the model performance based on a pid. This function
    - loads and combines forecast and realised data
    - calculated several key performance indicators (KPIs)
    These metric include:
        - RMSE,
        - bias,
        - NSME (model efficiency, between -inf and 1)
        - Mean absolute Error

    Args:
        pid (int): Prediction ID for a given prediction job
        start_time (datetime): Start time from when to retrieve the historic load prediction.
        end_time (datetime): Start time till when to retrieve the historic load prediction.

    Returns:
        Dictionary that includes a dictonary for each t_ahead.
        Dict includes enddate en window (in days) for clarification

    Example:
        To get the rMAE for the 24 hours ahead prediction: kpis['24h']['rMAE']
    """
    COMPLETENESS_REALISED_THRESHOLDS = 0.7
    COMPLETENESS_PREDICTED_LOAD_THRESHOLD = 0.7

    # Make database connection
    db = DataBase()
    log = logging.get_logger(__name__)

    pj = db.get_prediction_job(pid)

    # Apply default parameters if none are provided
    if start_time is None:
        start_time = datetime.utcnow() - timedelta(days=1)
    if end_time is None:
        end_time = datetime.utcnow()

    # Get realised load data
    realised = db.get_load_pid(pj["id"], start_time, end_time, "15T")

    # Get predicted load
    predicted_load = db.get_predicted_load_tahead(pj, start_time, end_time)

    # If predicted is empty, exit
    if len(predicted_load) == 0:
        raise ValueError(
            "Found no predicted load for pid {} between {} and {}!".format(
                pj["id"], start_time, end_time
            )
        )

    # If realised is empty, exit
    if len(realised) == 0:
        raise ValueError(
            "Found no realised load for pid {} between {} and {}!".format(
                pj["id"], start_time, end_time
            )
        )

    # Calculate completeness en raise exception if completeness does not meet requirements
    completeness_realised = calc_completeness(realised)

    # Interpolate missing data if needed
    realised = realised.resample("15T").interpolate(limit=3)

    # Calculate completeness for realised load
    completeness_predicted_load = calc_completeness(predicted_load)

    # Combine the forecast and the realised to make sure indices are matched nicely
    combined = pd.merge(realised, predicted_load, left_index=True, right_index=True)

    # TODO: make basecase calculation optionalm only if there was data available 7 days before
    # Add basecase (load in same time period 7 days ago)
    basecase = db.get_load_pid(
        pj["id"], start_time - timedelta(days=7), end_time - timedelta(days=7), "15T"
    ).shift(periods=7, freq="d")
    basecase = basecase.rename(columns=dict(load="basecase"))

    combined = combined.merge(basecase, how="left", left_index=True, right_index=True)

    # Raise exception in case of constant load
    if combined.load.nunique() == 1:
        raise Exception("The load is constant!")

    # Define output dictonary
    kpis = dict()

    # Extract t_aheads from predicted_load,
    # Make a list of tuples with [(forecast_xh, stdev_xh),(..,..),..]
    hor_list = [
        ("forecast_" + t_ahead, "stdev_" + t_ahead)
        for t_ahead in set(col.split("_")[1] for col in predicted_load.columns)
    ]

    # cast date to int
    date = pd.to_datetime(end_time)

    # Calculate model metrics and add them to the output dictionary
    log.info("Start calculating kpis")
    for hor_cols in hor_list:
        t_ahead_h = hor_cols[0].split("_")[1]
        fc = combined[hor_cols[0]]  # load predictions
        st = combined[hor_cols[1]]  # standard deviations of load predictions
        completeness_predicted_load = calc_completeness(fc.to_frame(name=t_ahead_h))
        kpis.update(
            {
                t_ahead_h: {
                    "RMSE": metrics.rmse(combined["load"], fc),
                    "bias": metrics.bias(combined["load"], fc),
                    "NSME": metrics.nsme(combined["load"], fc),
                    "MAE": metrics.mae(combined["load"], fc),
                    "rMAE": metrics.r_mae(combined["load"], fc),
                    "rMAE_highest": metrics.r_mae_highest(combined["load"], fc),
                    "rMNE_highest": metrics.r_mne_highest(combined["load"], fc),
                    "rMPE_highest": metrics.r_mpe_highest(combined["load"], fc),
                    "rMAE_lowest": metrics.r_mae_lowest(combined["load"], fc),
                    "skill_score_basecase": metrics.skill_score(
                        combined["load"],
                        combined["basecase"],
                        np.mean(combined["basecase"]),
                    ),
                    "skill_score": metrics.skill_score(
                        combined["load"], fc, np.mean(combined["basecase"])
                    ),
                    "skill_score_positive_peaks": metrics.skill_score_positive_peaks(
                        combined["load"], fc, np.mean(combined["basecase"])
                    ),
                    "skill_score_positive_peaks_basecase": metrics.skill_score_positive_peaks(
                        combined["load"],
                        combined["basecase"],
                        np.mean(combined["basecase"]),
                    ),
                    "franks_skill_score": metrics.franks_skill_score(
                        combined["load"], fc, combined["basecase"]
                    ),
                    "franks_skill_score_peaks": metrics.franks_skill_score_peaks(
                        combined["load"], fc, combined["basecase"]
                    ),
                    "load_range": combined["load"].max() - combined["load"].min(),
                    "frac_in_1sdev": metrics.frac_in_stdev(combined["load"], fc, st),
                    "frac_in_2sdev": metrics.frac_in_stdev(
                        combined["load"], fc, 2 * st
                    ),
                    "completeness_realised": completeness_realised,
                    "completeness_predicted": completeness_predicted_load,
                    "date": date,  # cast to date
                    "window_days": np.round(
                        (end_time - start_time).total_seconds() / 60.0 / 60.0 / 24.0
                    ),
                }
            }
        )

        if completeness_realised < COMPLETENESS_REALISED_THRESHOLDS:
            log.warning(
                "Completeness realised load too low",
                prediction_id=pj["id"],
                start_time=start_time,
                end_time=end_time,
                completeness=completeness_realised,
                completeness_threshold=COMPLETENESS_REALISED_THRESHOLDS,
            )
            set_incomplete_kpi_to_nan(kpis, t_ahead_h)
        if completeness_predicted_load < COMPLETENESS_PREDICTED_LOAD_THRESHOLD:
            log.warning(
                "Completeness predicted load too low",
                prediction_id=pj["id"],
                horizon=t_ahead_h,
                start_time=start_time,
                end_time=end_time,
                completeness=completeness_predicted_load,
                completeness_threshold=COMPLETENESS_PREDICTED_LOAD_THRESHOLD,
            )
            set_incomplete_kpi_to_nan(kpis, t_ahead_h)

    # Return output dictionary
    return kpis


def set_incomplete_kpi_to_nan(kpis, t_ahead_h):
    """
    Checks the given kpis for completeness and sets to nan if this not true

    :param kpis: the kpis
    :param t_ahead_h: t_ahead_h
    :return: -
    """
    kpi_metrics = list(kpis[t_ahead_h].keys())
    # Set to nan
    for kpi in kpi_metrics:
        if kpi != "completeness":
            kpis[t_ahead_h].update({kpi: np.nan})
