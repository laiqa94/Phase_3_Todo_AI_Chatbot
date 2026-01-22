---
id: 7
title: "Add debug logging to API calls"
stage: red
date: 2026-01-19
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: Claude Sonnet 4.5
command: manual
labels: ["api", "debugging", "logging", "bug-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/lib/apiServer.ts"
tests: []
---

# Add debug logging to API calls

## User Intent
Add debug logging to help troubleshoot the fetch failed error in API calls

## Technical Approach
Added debug logging to the apiFetchServer function to help identify what URL is being attempted when the fetch fails. This will help diagnose connection issues with the backend service.

## Code Changes
Modified frontend/lib/apiServer.ts:
- Added debug logging to show the full URL being fetched in development mode
- Maintained existing error handling and fallback logic
- Added console.log to show the URL being attempted

## Outcome & Impact
The API calls will now log the URL being attempted in development mode, which will help diagnose connectivity issues. The core functionality remains unchanged - fallback mock data should still be used when the backend is unreachable.

## Files Modified
- frontend/lib/apiServer.ts

## Tests Summary
No automated tests were run as this was a logging addition.

## Next Steps
- Monitor the logs to see the actual URL being attempted
- Check if backend service is running at expected location
- Verify that fallback mechanism works as expected

## Reflection
Adding debug logging is helpful for troubleshooting network connectivity issues in development environments.

## Failure Modes Observed
None observed during implementation.

## Next Experiment
Monitor the logs to determine the exact cause of the fetch failures.