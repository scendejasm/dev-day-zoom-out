# How to Try Out Prefect Resources

First enable the setting to use the experimental version of this feature:

`export PREFECT_EXPERIMENTS_LINEAGE_EVENTS_ENABLED=True`

Then navigate to the explore page in Prefect Cloud:

[https://app.prefect.cloud/account/your-account-id/workspace/your-workspace-id/explore](https://app.prefect.cloud/account/your-account-id/workspace/your-workspace-id/explore)

## 3 Ways to Emit Resource Events:

1. With [result persistence](https://docs.prefect.io/v3/develop/results#configuring-result-persistence) turned on, Prefect will automatically start to receive resource information about your flows.
2. Use our DBT integration to emit resource events automatically whenever DBT is run. See [Track 2 Session 2](https://github.com/PrefectHQ/dev-day-zoom-out/tree/main/track_2_operationalize_workflows/session_2_integrate_dbt) for more information.
3. Manually emit the resource events like I do in [this example](https://github.com/PrefectHQ/dev-day-zoom-out/blob/main/track_2_operationalize_workflows/session_1_zoom_in/get_mlb_data.py#L40):
  ```python3
  @task
  async def get_highlighted_teams_data_from_s3() -> pd.DataFrame:
      s3_bucket_block = await S3Bucket.load("mlb-raw-data")
      s3_bucket_path = await s3_bucket_block.upload_from_path("2025-01-02-143-alluring-dragonfly-boxscore.json")
      downloaded_file_path = await s3_bucket_block.download_object_to_path(
          s3_bucket_path, "highlighted_team_data.json"
      )
  
      await emit_lineage_event(
          event_name="Get Highlighted Teams Data from S3",
          upstream_resources=[HIGHLIGHTED_TEAMS_S3_FILE],
          downstream_resources=None,
          direction_of_run_from_event="downstream",
      )
  ```
Above, the S3 resource is upstream of my flow. So, for the direction of run from the resource event, I say 'downstream' because my flow is downstream of the data in this S3 bucket.


A resource should look something like the examples from [resources.py](resources.py).


```python3
OPEN_METEO_ELEVATION_API = {
    "prefect.resource.id": "api://api.open-meteo.com/v1/elevation",
    "prefect.resource.lineage-group": "global",
    "prefect.resource.role": "api",
    "prefect.resource.name": "api.elev.open-meteo.elevation",
}
```

A rule of convention is to start the resource ID with "`category_name://`resource_id". For this API, I use part of the request URL to build the resource ID.


