# [WORK-IN-PROGRESS] tap-easybill

## To do
- Add `_sdc_extracted_at` timestamps
- Add metrics and info logging
- Handle empty state / full table replication
- Improve limiting API pages, potentially save number of changed pages in last run
- Check for string encoding problems
- Use config for authorization
- Add proper timezone to timestamps
- Flatten (or otherwise handle) nested objects, most importantly for documents endpoint
  - Actually, could let Stitch handle denesting as well https://www.stitchdata.com/docs/data-structure/nested-data-structures-row-count-impact
