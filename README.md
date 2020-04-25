# tap-easybill

## To do
- Remember state, potentially use `edited_at` property of document, for other endpoints simply creation date
- Check for string encoding problems
- Use config for authorization
- Add proper timezone to timestamps
- Flatten (or otherwise handle) nested objects, most importantly for documents endpoint
  - Actually, could let Stitch handle denesting as well https://www.stitchdata.com/docs/data-structure/nested-data-structures-row-count-impact
- Use config for specifying key properties?
