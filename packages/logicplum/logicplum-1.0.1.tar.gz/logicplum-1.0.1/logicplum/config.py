HOST_NAME = "https://staging-api.logicplum.com/"

PROJECT_CREATE = "api/v2/external/project"
MODEL_TRAIN = "api/v2/external/data/training"
MODEL_TRAIN_STATUS = "api/v2/external/data/training"
MODEL_LIST = "api/v2/external/model/list"
DEPLOY = "api/v2/external/deployment"
DEPLOY_LIST = "api/v2/external/deployment/list"
MODEL_SCORE = "api/v2/external/data/scoring"
MODEL_BLUEPRINT = "api/v2/external/blueprint"

ALLOWED_ENVIRONMENTS: dict = {
    "local": "http://127.0.0.1:8000/api/v2/", 
    "sandbox": "https://sb-api.logicplum.com/api/v2/", 
    "staging": "https://staging-api.logicplum.com/api/v2/", 
    "production": "https://api.logicplum.com/api/v2/",
}

YAML_TOKEN_KEY: str = "token"
