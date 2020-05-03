# [WORK-IN-PROGRESS] tap-easybill

## To do
- Make clever guess on relevant page range, maybe (max page - X) and set X in config? As percentage?
- Add `_sdc_extracted_at` timestamps
- Handle empty state / full table replication
- Check for string encoding problems
- Use config for authorization
- Add proper timezone to timestamps
- Flatten (or otherwise handle) nested objects, most importantly for documents endpoint
  - Actually, could let Stitch handle denesting as well https://www.stitchdata.com/docs/data-structure/nested-data-structures-row-count-impact
