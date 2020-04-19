echo $STITCH_CONFIG_FILE | base64 -d > target_config.json
tap-easybill --config tap_config.json | target-stitch --config target_config.json
