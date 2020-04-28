# [WORK-IN-PROGRESS] tap-easybill

## To do
- Remember state, potentially use `edited_at` property of document, for other endpoints simply creation date
  - !! Need to figure out how to keep track of state for both ordered and unordered replication keys
  - Cannot limit bulk API call by id or date, need to make clever guess on
  relevant page range, maybe (max page - X) and set X in config? As percentage?
  - How to differentiate reliably between full replication and incremental?
  - Bulk API responses are sorted by id
- Check for string encoding problems
- Use config for authorization
- Add proper timezone to timestamps
- Flatten (or otherwise handle) nested objects, most importantly for documents endpoint
  - Actually, could let Stitch handle denesting as well https://www.stitchdata.com/docs/data-structure/nested-data-structures-row-count-impact
- Use config for specifying key properties?
