from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
QUIZ_DIR = env.str("QUIZ_DIR", default="quiz-questions")
USE_PROXY = env.bool("USE_PROXY", False)
BOT_PROXY = env.str("BOT_PROXY") if USE_PROXY else None
