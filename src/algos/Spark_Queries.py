from pyspark.sql.functions import col
import json
def queryDataframe(df, conditions):
    result_df = df

    for key, value in conditions.items():
        result_df = result_df.filter(col(key) == value)

    return result_df.toJSON().map(lambda j: json.loads(j)).collect()
