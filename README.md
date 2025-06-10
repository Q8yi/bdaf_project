# How impactful are tweets made by influential figures on blockchain prices

```shell
npm install
pip3 install -r requirements.txt
python app.py

```


```shell
Data files under folder dataset/network/network_data explanation:
The following represent what each files contained :

The explanantion follows the following format:
    <Files name format> :
        cols: representation

<network_name>_avg_all.csv columns include :
1) avg_value: The amount of tokens transferred  on average for the day
2) avg_fee: The fee amount paid for the transfer on average for the day
3) Block_timestamp: The block\'s date

<network_name>_transac_all.csv columns include :
1) date : block\s date
2) avg_count : transaction count on the particular network on average each day

<network_name>_gas_all.csv columns include :
1) date : block\s date
2) avg_count : transaction count on the particular network on average each day
3) some files contain avg_base_fee_per_gas: base fee per gas on average each day (due to lack of data , we will be ignoring this column)


<network_name>_gas_all.csv columns include :
1) date : block\'s date
2) avg_gas_price_in_wei : Gas price provided by the sender in Wei on average each day
3) avg_value_in_wei: Value transferred in Wei on average each day

Data files under folder dataset/tweets explanation:
1) cleaned_tweets.csv
-> processed and merged all files in filtered tweets
-> transforming object type columns to integer type (preparation for machine learning)


Data files under folder datasets/network/merged explanation:
each file represent csv output of merging every data in network/network_data with tweets/cleaned_tweets.csv and network/prices with tweets/cleaned_tweets.csv
-> the purpose is to ease the process of training and testing in machine learning models


```

```shell
under scripts folder

1) network_data_retrieval.sql
please copy paste each code block to the respective datasets in the following google bigquery link:
https://cloud.google.com/blockchain-analytics/docs/supported-datasets

the codes block is meant to run in google cloud, to retrieve each respective dataset mentioned in the comment line above each block

2) analysis.ipynb
- represent different correlation analysis for each respective network_data and network > prices dataset with each tweets posted by different users

```