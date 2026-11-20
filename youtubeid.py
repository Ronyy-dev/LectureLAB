def youtube_id(url) :
    for char in ["watch?v=", "youtu.be/","/shorts/"] :
        if char in url :
            after=url.split(char)[1]
            code=after[:11]
            if len(code) == 11 :
                return code
            return None
    return None        