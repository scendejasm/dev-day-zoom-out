# Session 3: Zoom Out

## Overview
This session explores Prefect's Operational Intelligence capabilities, zooming out to take a high-level look at your entire workflow ecosystem. You'll learn how Prefect can help you to visualize dependencies, track system-wide performance through metrics and SLAs, and trace the lineage of data to understand how issues can cascade through your pipeline. We'll explore how teams can use these insights to spot problems early, gain deeper insight into their causes, and automate responses to fix issues before they impact your business.

Prerequisites:
- Complete the instructions in the README.md file in the root of the dev-day-zoom-out directory to set up your environment.
- Complete the instructions in the README.md file in the session_1_zoom_intrack 2 folder to set up your environment.
- If you would like to create lineage events from results, you will need to set the `PREFECT_LINEAGE_ENABLED` environment variable to `true`. You can do this by running `prefect config set PREFECT_LINEAGE_ENABLED=true`.

## Project Contents
- `get_mlb_data_results.py`: A script that fetches and analyzes MLB game statistics using the MLB Stats API.
- `prefect.yaml`: A configuration file for the Prefect agent.
- `new_game_data.py`: A flow that fetches and analyzes MLB game statistics using the MLB Stats API.
- `resources`: A model for how to create a Prefect resource manually.
- `snowflake_helper.py`: Tasks that manages interactions with Snowflake.


