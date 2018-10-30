# Insight DevOps Puzzle

## Architecture

```shell
+----------------+                          +----------------+
|                | Pub +--------------+ Sub |                |
|   Web Server   +----->   RabbitMQ   +----->   Flask App    |
|                |     +--------------+     |                |
+----------------+                          +--------+-------+
                                                     |
                                                     |
                                                  +--+--+
                                                  |     |
                                                  | DB  |
                                                  |     |
                                                  +-----+
```

## References
* https://docs.docker.com/compose/install/#install-compose
