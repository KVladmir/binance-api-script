# Python script for binance api.
- ### influxdb.env example:
  ```DOCKER_INFLUXDB_INIT_MODE=setup
   DOCKER_INFLUXDB_INIT_USERNAME=my-user
   DOCKER_INFLUXDB_INIT_PASSWORD=my-password
   DOCKER_INFLUXDB_INIT_ORG=my-org
   DOCKER_INFLUXDB_INIT_BUCKET=my-bucket
   DOCKER_INFLUXDB_INIT_RETENTION=1m
   DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=my-super-secret-auth-token
- ### config.json example:
    ```yaml
        {
          "url": "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search",
          "dbUrl": "http://influxdb:8086",
          "dbTimeout": "10000",
          "rows": "10",
          "pages": "1",
          "bucket": "my_bucket",
          "token": "my_token",
          "org": "my_org",
          "bparams": [
            {
              "asset": "USDT",
              "fiat": "some_fiat",
              "tradeType": "BUY",
              "payTypes": [
                "some_bank"
              ]
            },
            {
              "asset": "USDT",
              "fiat": "another_fiat",
              "tradeType": "SELL",
              "payTypes": [
                "another_bank"
              ]
            }
          ]
        }