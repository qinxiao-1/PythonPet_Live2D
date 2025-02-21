import os

CURRENT_DIRECTORY = os.path.split(__file__)[0]
RESOURCES_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "../Resources")

temp_aduio_path = r'.\Resources\Audio\temp.wav'

Epsilon_v2 = r".\Resources\V2\Epsilon\Epsilon.model.json"
haru_v2 = r".\Resources\V2\haru\haru.model.json"
hibiki_v2 = r".\Resources\V2\hibiki\hibiki.model.json"
kasumi2_v2 = r".\Resources\V2\kasumi2\kasumi2.model.json"

Hiyori_v3 = r".\Resources\V3\Hiyori\Hiyori.model3.json"

# Open Ai
OpenAIKey = '1'
OpenAIUrl = "http://61.157.13.79:11434/v1"