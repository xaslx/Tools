import replicate
from dotenv import load_dotenv, get_key
load_dotenv('.env')

REPLICATE_API_TOKEN: str = get_key('.env', 'REPLICATE_API_TOKEN')
print(REPLICATE_API_TOKEN)

res = replicate.run('stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b',
                                input={
                                    'width': 1024,
                                    'height': 1024,
                                    'prompt': 'Elon Musk drink coffee'
                                })
image = res[0]
print(image)
print(res)