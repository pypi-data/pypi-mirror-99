# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# python3
"""Contains functions useful to design media experiments.

Specially useful when designing media experiments to activate a propensity model
or a customer lifetime value model built using GA360, Firebase or CRM data.
"""

from typing import Optional, Sequence
import numpy as np
import pandas as pd
from statsmodels.stats import gof
from statsmodels.stats import power
from gps_building_blocks.ml import utils


def calc_chisquared_sample_size(
    baseline_conversion_rate_percentage: np.float64,
    expected_uplift_percentage: np.float64,
    power_percentage: Optional[np.float64] = 80,
    confidence_level_percentage: Optional[float] = 95) -> np.float64:
  """Estimates the minimum sample size when the KPI is conversion rate.

  Estimated sample size using the Chi-squared test of proportions is the
    minimum required for either a Test or a Control group in an A/B test.

  Args:
    baseline_conversion_rate_percentage: Baseline conversion rate as a
      percentage.
    expected_uplift_percentage: Expected uplift of the media experiment on the
      baseline conversion rate as a percentage.
    power_percentage: Statistical power of the Chi-squared test as a percentage.
    confidence_level_percentage: Statistical confidence level of the Chi-squared
      test as a percentage.

  Returns:
    sample_size: Estimated minimum sample size required for either a Test or
      a Control group.
  """
  null_probability = baseline_conversion_rate_percentage / 100
  alternative_probability = (
      null_probability * (100 + expected_uplift_percentage) / 100)
  alpha_proportion = (100 - confidence_level_percentage) / 100
  power_proportion = power_percentage / 100

  effect_size = gof.chisquare_effectsize(
      probs0=[null_probability, 1 - null_probability],
      probs1=[alternative_probability, 1 - alternative_probability],
      correction=None,
      cohen=True,
      axis=0)
  power_test = power.GofChisquarePower()
  sample_size = power_test.solve_power(
      effect_size=effect_size,
      nobs=None,
      alpha=alpha_proportion,
      power=power_proportion,
      n_bins=2)

  return np.ceil(sample_size)


def calc_chisquared_sample_sizes_for_bins(
    labels: np.ndarray,
    probability_predictions: np.ndarray,
    number_bins: Optional[int] = 3,
    uplift_percentages: Optional[Sequence[float]] = (10, 20),
    power_percentages: Optional[Sequence[float]] = (80, 90),
    confidence_level_percentages: Optional[Sequence[float]] = (90, 95)
) -> pd.DataFrame:
  """Calculates statistical sample sizes for the bins defined on predictions.

  These sample sizes for the bins defined on the predicted probabilities are
    estimated using the Chi-squared test of proportions for each combination
    of uplift_percentage, power_percentage and confidence_level_percentage.
    These sizes could be used as the minimum required size for each Test or
    Control group when designing an experiment to target users from ech of these
    bins of predictions.

  Args:
    labels: An array of true binary labels represented by 1.0 and 0.0.
    probability_predictions: An array of predicted probabilities between 0.0 and
      1.0.
    number_bins: Number of bins that we want to divide the ranked predictions
      into. Default is deciles (3 bins) such that the 1st bin contains the
      highest 1/3rd of the predictions (High Propensity group), the 2nd bin
      contains the next 1/3rd of the predictions (Medium Propensity group) and
      the last bin contains the lowest 1/3rd of the predictions (Lowest
      Propensity group).
    uplift_percentages: List of different expected uplift percentages.
    power_percentages: List of different statistical powers for the test.
    confidence_level_percentages: List of different statistical confidence
      levels for the test.

  Returns:
    bin_metrics: Following metrics calculated for each bin of the predictions.
     bin_number: Bin number starting from 1,
     bin_size: Total numbers of instances in the bin,
     conversion_rate: Proportion of positive instances out of all the instances
       in the bin (precision),
     expected_uplift: Expected uplift_percentage,
     power_percentage: Statistical power of the test,
     confidence_level_percentage: Statistical confidence level of the test,
     sample_size: Statistical sample size required.
  """
  utils.assert_label_values_are_valid(labels)
  utils.assert_prediction_values_are_valid(probability_predictions)
  utils.assert_label_and_prediction_length_match(labels,
                                                 probability_predictions)

  # separate the probability_predictions into bins of equal size
  bins = pd.qcut(probability_predictions, q=number_bins, labels=False)
  binned_data = pd.DataFrame(
      list(zip(labels, probability_predictions, bins)),
      columns=['label', 'prediction', 'bin_number'])

  # calculate the conversion rate for each bin
  total_instances = (
      binned_data[['bin_number', 'label']].groupby('bin_number').count())
  total_instances.columns = ['bin_size']
  total_instances = total_instances.reset_index()
  positive_instances = (
      binned_data.loc[binned_data['label'] > 0][[
          'bin_number', 'label'
      ]].groupby('bin_number').count())
  positive_instances.columns = ['positive_instances']
  positive_instances = positive_instances.reset_index()

  bin_conv_rate = pd.merge(
      total_instances, positive_instances, on='bin_number', how='left')
  bin_conv_rate.fillna(0, inplace=True)
  bin_conv_rate['conversion_rate'] = round(
      (bin_conv_rate['positive_instances'] / bin_conv_rate['bin_size'] * 100),
      2)

  # reverse the order of bin numbers such that bin 1 has the highest
  # predicted probability
  bin_conv_rate['bin_number'] = number_bins - bin_conv_rate['bin_number']
  bin_conv_rate = bin_conv_rate.sort_values(['bin_number'
                                            ]).reset_index(drop=True)

  bin_metrics_list = list()
  for bin_number in bin_conv_rate['bin_number']:
    conv_rate = bin_conv_rate['conversion_rate'][bin_number - 1]
    bin_size = bin_conv_rate['bin_size'][bin_number - 1]
    for uplift_percentage in uplift_percentages:
      for power_percentage in power_percentages:
        for confidence_level_percentage in confidence_level_percentages:
          sample_size = calc_chisquared_sample_size(
              conv_rate, uplift_percentage, power_percentage,
              confidence_level_percentage)
          bin_metrics_list.append(
              (bin_number, bin_size, conv_rate, uplift_percentage,
               power_percentage, confidence_level_percentage, sample_size))

  return pd.DataFrame(
      bin_metrics_list,
      columns=[
          'bin_number', 'bin_size', 'conv_rate_percentage', 'uplift_percentage',
          'power_percentage', 'confidence_level_percentage', 'sample_size'
      ])
