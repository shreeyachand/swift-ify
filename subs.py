taylors_version_equivalents = {
    # NO DELUXE VERSIONS ACCOUNTED FOR AS OF RIGHT NOW

    # Fearless 1-13
    '6Eu31gddWw0gOGO506pJYA':'77sMIMlNaSURUAXq5coCxE', # Fearless
    '4t0OI7XrODjSkAu3bTPmWj':'2nqio0SfWg6gh2eCtfuMa5', # Fifteen
    '1vrd6UOGamcKNGnSHJQlSt':'6YvqWjhGD8mB5QXcbcUKtx', # Love Story
    '4WXzzCof26KJLTK5kK53dS':'550erGcdD9n6PnwxrvYqZT', # Hey Stephen
    '6wn61Fzx9XMxQmieLpoIhW':'5YL553x8sHderRBDlm3NM3', # White Horse
    '3GCL1PydwsLodcpv0Ll1ch':'1qrpoAMXodY6895hGKoUpA', # YBWM
    '49mWEy5MgtNujgT7xU3emT':'7HC7R2D8WjXVcUHJyEGjRs', # Breathe
    '3rnI1UCyGJvUTVvT97VQr5':'0k0vFacOHNuArLWMiH60p7', # Tell Me Why
    '0HmCuN0Z3OX1Qrz43FLOPL':'6iiAfo4wTA2CVC3Uwx9uh8', # You're Not Sorry
    '5P4wWhUYWM0IaVYLuZxdar':'22bPsP2jCgbLUvh82U0Z3M', # The Way I Loved You
    '47HtKpfzpAt8rQjjXWotFj':'1msEuwSBneBKpVCZQcFTsU', # Forever & Always
    '3esA216TyLHEkNiBCeCmcg':'6ON9UuIq49xXY9GPmHIYRp', # The Best Day
    '1yACRKAwlXWhXXFUSkvzhD':'3ExweHKZF9B752DPQByRVT',  # Change
    # Fearless Platinum
    '08gavXombT6KR0af88i9tA':'2m3ObD945KvpE5y9A1eUWm', # Jump Then Fall
    '2IZ00ed83ygPIiacYScWUE':'0tQ9vBYpldCuikPsbgOVKA', # Untouchable
    '46HGgtwmmuEB8mvDCyjyAc':'01QdEx6kFr78ZejhQtWR5m', # Forever & Always PV
    '4pl5zcqCv4vc3cB7M4MZ6f':'1n2wszmJyVkw6FHqyLnQsY', # Come In With The Rain
    '14Bljc3pOOG0xQX3wqhLN9':'51A8eKvvZz9uydvIZ7xRSV', # Superstar
    '0xvsgzM8AtBtRHZm5rav8A':'1cSFlSBdpT4F5vb1frQ231', # The Other Side Of The Door
    '4pFvEWbjBpPUdYRQly0THs':'2JoJrsEV15OzbijS47lids', # Today Was A Fairytale
    # Wildest Dreams
    '59HjlYCeBsxdI0fcm3zglw':'1Ov37jtRQ2YNAe8HzfczkL'
}

def fetch_tv_id(id):
    if id in taylors_version_equivalents.keys():
        return taylors_version_equivalents[id]
    return -1