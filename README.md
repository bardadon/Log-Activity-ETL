# Log-Activity-ETL

This ETL process is used for transferring data from MySQL's binary log and into Google's BigQuery for analysis.
The activity within the company is simulated using a stored procedure.

Check out my Medium article for more information about this process:
https://medium.com/@bdadon50/data-engineering-project-etl-for-analyzing-log-activity-a9dff9e7b044

## Project Architecture


## Project Steps
1. Extract Data Using MySQL’s Binary Log
2. Load Data to Google’s Cloud Storage for Backup
3. Load Data to Google’s BigQuery for Analyzing

## Running the ETL
1. Generate a service account configuration file from Google called: ServiceKey_GoogleCloud.json
2. Create a file called: pipeline.conf with all the configurations required for logging into MySQL(as shown in the article)
3. Run the command:

```
bash run_etl.sh
```

## End Result
1. Log activity data ready to be analyzed in Google’s BigQuery:
![Untitled(46)](https://user-images.githubusercontent.com/65648983/195849208-b30ac6ed-90bf-4913-8467-efa44c5f9067.png)

2. Backup data in Google’s Cloud Storage Bucket:
![Untitled(47)](https://user-images.githubusercontent.com/65648983/195849278-5da8e102-a163-4bc6-aa68-bdce39df761e.png)
