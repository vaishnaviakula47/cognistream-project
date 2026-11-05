# Developer Activity Monitoring

## Introduction

The CogniStream activity monitoring module records developer coding activities.

## Activities Tracked

1. Coding session start time
2. Coding session duration
3. Number of task switches
4. Number of development errors
5. Number of breaks

## Data Collection Process

The `ActivityMonitor` class records developer activities through its methods.

The collected information is stored in `developer_activity.csv`.

## Dataset Fields

| Field | Description |
|---|---|
| timestamp | Session start time |
| session_minutes | Session duration |
| switch_count | Number of task switches |
| error_count | Number of errors |
| break_count | Number of breaks |

## Benefits

- Helps analyze developer work patterns.
- Identifies frequent task switching.
- Supports focus-state analysis.
- Provides data for cognitive-load estimation.

## Conclusion

Activity monitoring provides structured developer activity data for CogniStream.
