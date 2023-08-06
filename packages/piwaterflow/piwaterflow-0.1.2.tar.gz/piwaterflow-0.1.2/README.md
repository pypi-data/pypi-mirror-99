# PiWaterflow
This is a resilient watering system, executed in a Raspberry Pi to control irrigation valves using relays.
It's intended to be executed periodically (i.e. cron every 5 minutes).
- Requirements:
  - Raspberry Pi (any model)
  - Relays to control the valves
  - Optional control relay to enable alternative power inverter
- It supports 2 watering programs every day.
  - Programs can be forced at any time.
- Valves can be manually triggered.
- Programs, forced programs and manual Valves can be manually stopped.
- Metrics can be emitted to influxdb to register actions (programs and valves).
- This package fits with wwwaterflow, so that it can be controlled via HTTP page.
