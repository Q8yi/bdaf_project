#TO RUN THIS, PLEASE GO TO https://cloud.google.com/blockchain-analytics/docs/supported-datasets
#copy paste each code block according to network and file
#and run it at google bigquery

#SOLANA NETWORK > token_transfers
#output file solana<year>.csv
SELECT *
FROM `bigquery-public-data.crypto_solana_mainnet_us.token_transfers`
WHERE block_timestamp BETWEEN TIMESTAMP("2020-01-01") AND TIMESTAMP("2024-12-31 23:59:59");

#SOLANA NETWORK > Blocks
#output file solana_transac_<year>.csv
SELECT
  DATE(block_timestamp) AS date,
  AVG(transaction_count) AS avg_count
FROM
  `bigquery-public-data.crypto_solana_mainnet_us.Blocks`
WHERE
  block_timestamp BETWEEN TIMESTAMP("2024-01-01") AND TIMESTAMP("2024-12-31 23:59:59")
GROUP BY
  date
ORDER BY
  date;

  #POLYGON NETWORK > blocks
  #OUTPUT FILE POLYGON_TRANSAC_<YEAR>.csv
  SELECT
  DATE(timestamp) AS date,
  AVG(transaction_count) AS avg_count,
  AVG(base_fee_per_gas) AS avg_base_fee_per_gas
FROM
  `bigquery-public-data.crypto_polygon.blocks`
WHERE
  timestamp BETWEEN TIMESTAMP("2024-01-01") AND TIMESTAMP("2024-12-31 23:59:59")
GROUP BY
  date
ORDER BY
  date;

  #POLYGON > transactions
  #OUTPUT FILE polygon_gas_<YEAR>.csv
  SELECT
  DATE(block_timestamp) AS date,
  AVG(gas_price) AS avg_gas_price_in_wei,
  AVG(value) AS avg_value_in_wei
FROM
  `bigquery-public-data.crypto_polygon.transactions`
WHERE
  block_timestamp BETWEEN TIMESTAMP("2021-01-01") AND TIMESTAMP("2021-12-31 23:59:59")
GROUP BY
  date
ORDER BY
  date;


  #ETH NETWORK > transactions
  # OUTPUT FILE eth_gas_<year>.csv
 #eth gas <year>
  SELECT
  DATE(block_timestamp) AS date,
  AVG(gas_price) AS avg_gas_price_in_wei,
  AVG(value) AS avg_value_in_wei
FROM
  `bigquery-public-data.crypto_ethereum.transactions`
WHERE
  block_timestamp BETWEEN TIMESTAMP("2024-01-01") AND TIMESTAMP("2024-12-31 23:59:59")
GROUP BY
  date
ORDER BY
  date;

  #eth > blocks
  #OUTPUT FILE eth_transac_<year>.csv
  SELECT
  DATE(timestamp) AS date,
  AVG(transaction_count) AS avg_count,
  AVG(base_fee_per_gas) AS avg_base_fee_per_gas
FROM
  `bigquery-public-data.crypto_ethereum.blocks`
WHERE
  timestamp BETWEEN TIMESTAMP("2020-01-01") AND TIMESTAMP("2020-12-31 23:59:59")
GROUP BY
  date
ORDER BY
  date;


  #doge network > transactions
  #output file : doge_avg_<year>.csv
  SELECT
  DATE(t.block_timestamp) AS date,
  AVG(t.fee) AS avg_fee,
  AVG(o.value) AS avg_value
FROM
  `bigquery-public-data.crypto_dogecoin.transactions` AS t,
  UNNEST(t.outputs) AS o
WHERE
  t.block_timestamp BETWEEN TIMESTAMP("2021-01-01") AND TIMESTAMP("2021-12-31 23:59:59")
GROUP BY
  date
ORDER BY
  date;

#DOGE NETWORK > blocks
  #OUTPUT FILE : doge_transac_<year>
  SELECT
  DATE(timestamp) AS date,
  AVG(transaction_count) AS avg_count
FROM
  `bigquery-public-data.crypto_dogecoin.blocks`
WHERE
  timestamp BETWEEN TIMESTAMP("2024-01-01") AND TIMESTAMP("2024-12-31 23:59:59")
GROUP BY
  date
ORDER BY
  date;


  #bitcoin > blocks
  #OUTPUT FILE: bit_transac_<year>.csv
  SELECT
  DATE(timestamp) AS date,
  AVG(transaction_count) AS avg_count
FROM
  `bigquery-public-data.crypto_bitcoin.blocks`
WHERE
  timestamp BETWEEN TIMESTAMP("2024-01-01") AND TIMESTAMP("2024-12-31 23:59:59")
GROUP BY
  date
ORDER BY
  date;

#BITCOIN > transactions
#OUTPUT FILE : bit_avg_<year>.csv
SELECT
  DATE(t.block_timestamp) AS date,
  AVG(t.fee) AS avg_fee,
  AVG(o.value) AS avg_value
FROM
  `bigquery-public-data.crypto_bitcoin.transactions` AS t,
  UNNEST(t.outputs) AS o
WHERE
  t.block_timestamp BETWEEN TIMESTAMP("2024-01-01") AND TIMESTAMP("2024-12-31 23:59:59")
GROUP BY
  date
ORDER BY
  date;
