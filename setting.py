from rhino_v2_utilis.handler.redis_handler import CRedisHandler
import config
import json
redis_config = config.TASK_DB_CONFIG
redis_client = CRedisHandler(host=redis_config['ip'], port=redis_config["port"], db=redis_config["db_name"],password=redis_config["password"])
