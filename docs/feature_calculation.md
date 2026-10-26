Feature Calculation Examples

Objective

Document how useful features are calculated from sample developer activity data.

Example Features

1. Session Duration

Session Duration = Session End Time - Session Start Time

2. Task Switching Frequency

Task Switching Frequency = Number of Task Switches / Session Duration in Hours

3. Break Duration

Break Duration = Break End Time - Break Start Time

4. Coding Activity Percentage

Coding Activity Percentage = (Coding Activity Time / Observed Session Time) * 100

Validation

- Check for missing timestamps.
- Confirm duration values are non-negative.
- Avoid dividing by zero.
- Verify calculations using sample records.

Expected Output

A documented set of feature definitions and calculation examples.

Note

Feature definitions must remain consistent across the dataset and dashboard.
