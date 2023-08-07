-- Copyright 2021 Google LLC
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--      http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.

-- Calculate statistics for categorical variables in the Facts table in BigQuery.
-- Facts table is created by the
-- DataExplorationPipeline of the MLWindowingPipeline tool. For more info:
-- https://github.com/google/gps_building_blocks/tree/master/py/gps_building_blocks/ml/data_prep/ml_windowing_pipeline
--
-- Query expects following parameters:
--  bq_facts_table: Full path to the Facts Table in BigQuery. Ex: project.dataset.table.
--  categorical_fact_list: A comma separated list of categorical fact names to calculate
--  statistics for.
--  number_top_categories: Number of top value levels to consider for each categorical fact.

WITH
  FactCount AS (
    SELECT
      FORMAT_TIMESTAMP('%Y-%m-%d', ts) AS date,
      name,
      value,
      COUNT(*) AS record_count
    FROM `{bq_facts_table}`
    GROUP BY date, name, value
  ),
  ValueRank AS (
    SELECT
      name,
      value,
      RANK() OVER (PARTITION BY name ORDER BY SUM(record_count) DESC) AS rank
      FROM FactCount
      GROUP BY name, value
  ),
  ValueRankModified AS (
    SELECT
      name,
      value,
      IF(rank <= {number_top_categories}, rank, NULL) AS rank
    FROM ValueRank
  ),
  TotalCount AS (
    SELECT
      date,
      name,
      SUM(record_count) AS total_record_count
    FROM FactCount
    GROUP BY date, name
  ),
  FactCountAndRank AS (
    SELECT
      FactCount.date,
      FactCount.name,
      FactCount.value,
      FactCount.record_count,
      ValueRankModified.rank
    FROM FactCount
    INNER JOIN ValueRankModified
      ON FactCount.name = ValueRankModified.name AND FactCount.value = ValueRankModified.value
  ),
  FactCountAndRankAndTotalCount AS (
    SELECT
      FactCountAndRank.date,
      FactCountAndRank.name,
      FactCountAndRank.value,
      FactCountAndRank.record_count,
      FactCountAndRank.rank,
      TotalCount.total_record_count
    FROM FactCountAndRank
    INNER JOIN TotalCount
      ON FactCountAndRank.date = TotalCount.date AND FactCountAndRank.name = TotalCount.name
   )
SELECT
  date,
  name AS fact_name,
  IF(rank IS NULL, "[other]", CAST(value AS STRING)) AS category_value,
  IF(rank IS NULL, "[other]", CAST(rank AS STRING)) AS rank,
  -- to aggregate the record_count and total_record_count of multiple category_values renamed as
  -- '[other]'
  SUM(record_count) AS record_count,
  AVG(total_record_count) AS total_record_count,
  SAFE_DIVIDE(SUM(record_count), AVG(total_record_count)) * 100 AS percentage
FROM FactCountAndRankAndTotalCount
GROUP BY date, fact_name, category_value, rank
ORDER BY date;
