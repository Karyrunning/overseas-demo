from fake_useragent import UserAgent
# ua = UserAgent(verify_ssl=False)
print(UserAgent(use_cache_server=False).random)