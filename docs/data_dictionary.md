# Data Dictionary

## Purpose

This document describes the fields used to record developer activity for the CogniStream project.

## Dataset Fields

| Field Name | Description |
|---|---|
| developer_id | Anonymous developer identifier |
| date | Date of the activity |
| session_start | Start time of a coding session |
| session_end | End time of a coding session |
| active_minutes | Estimated active duration in minutes |
| interruption_count | Number of recorded interruptions |
| task_switch_count | Number of recorded task changes |
| break_minutes | Duration of breaks in minutes |

## Data Preparation

The dataset should be checked for missing values, duplicate records, invalid timestamps, and negative numerical values.

## Data Privacy

Use synthetic or authorized activity data. Do not store passwords, private messages, or source-code contents.

## Data Limitations

Activity data provides indirect indicators of developer work patterns. It cannot independently determine a person's actual cognitive load.

## Conclusion

A consistent data dictionary helps team members prepare, validate, and analyze activity records correctly.
