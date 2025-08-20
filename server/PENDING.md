# Flask Migration - Performance Improvements

## Summary
We've successfully migrated the Bottle server to Flask with full thread safety to solve image serving bottlenecks during fast scrolling. The new Flask server includes HTTP caching headers, per-image locking for thumbnail generation, and proper synchronization of all global state and database operations.

## Setup Checklist
- [ ] Install Flask: `pip install flask`
- [ ] Test original Bottle server still works (existing run command)
- [ ] Run Flask server: `python main_flask.py` (starts on port 8081)
- [ ] Temporarily update frontend to use `localhost:8081` instead of original port

## Testing Checklist
- [ ] Verify all API endpoints work identically on Flask server
- [ ] Test fast scrolling performance - should no longer block/freeze UI
- [ ] Check browser DevTools Network tab - images should show cache headers
- [ ] Verify thumbnail generation works correctly under concurrent load
- [ ] Test all CRUD operations (edit sessions, add tags, splits) work properly
- [ ] Confirm data integrity - no corruption from race conditions

## Deployment Checklist (After Testing)
- [ ] Switch frontend permanently to Flask server
- [ ] Update production run scripts to use Flask
- [ ] Remove/archive `main.py` (Bottle version) if Flask works well
- [ ] Document new port/startup process for future reference