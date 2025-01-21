# How to Try Out Prefect Resources

First enable the setting to use the experimental version of this feature:

`export PREFECT_EXPERIMENTS_LINEAGE_EVENTS_ENABLED=True`

Then navigate to the explore page in Prefect Cloud:

[https://app.prefect.cloud/account/your-account-id/workspace/your-workspace-id/explore](https://app.prefect.cloud/account/your-account-id/workspace/your-workspace-id/explore)

## 3 Ways to Emit Resource Events:

1. With [result persistence](https://docs.prefect.io/v3/develop/results#configuring-result-persistence) turned on, Prefect will automatically start to recieve resource information about your flows.
2. Use our DBT integration to emit resource events automatically whenever DBT is run. See Track 2 Session 2 for more information.
3. Manually emit the resouce events like I do in [this example](https://github.com/PrefectHQ/dev-day-zoom-out/blob/main/track_2_operationalize_workflows/session_1_zoom_in/get_mlb_data.py#L40).
