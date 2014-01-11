#coding: utf-8

from oauth2 import Client, Token, Consumer 
import twitter
import random

class Twitter:
    #動かない大図書館
    consumer_key = 'rNrawjoXo7UKRSYAcTrsLg'
    consumer_secret = 'rfow5X32GgnEG017Hji1hQ6P3bKZbtuvzA63ygtsLs'

    access_tokens = {
            "alatani":"15130994-9kupaKFQGhnC0hLtwevz2Uy9FTiMwu7V6sc8FlOS6",
            "na_arin":"299029754-yi2yuWlEqe3srSdMe7udC8bHZKSuPlcpViQ1ZWNc",
            "alatan_":"220958811-N0s8Ynn1J1LEhD6HOkR3IUZyFHksaJ0SXrvLoq0W"
            }
    access_token_secrets = {
            "alatani":"GaBhOXPd1iAtJyj2brSlW8LRXJ2HUEaiAOcaGkcbjY",
            "na_arin":"31evfUNxgF1vLlOdisldIpgRI724xZUgykEp9t2hb8",
            "alatan_":"sg1xTym5QCnzzQT9uMCCJfz7ilTjhU8KBJPmMDxVnw"
            }


    def createConnection(self,targetUser):
        api = twitter.Api(consumer_key=self.consumer_key,
                          consumer_secret=self.consumer_secret,
                          access_token_key=self.access_tokens[targetUser],
                          access_token_secret=self.access_token_secrets[targetUser]
                         )
        return api

    def __init__(self,screen_name="alatani"):
        self.api = self.createConnection(screen_name)

    def post(self,tweet):
        try:
            if isinstance(tweet,type("dummy")):
                self.api.PostUpdate(tweet)
        except:
            print "e"
            pass


    #statuses = api.GetFriendsTimeline(since_id=maxid)
    #api.CreateFavorite(status)


#splitter = SentenceSplitter()
if __name__ == '__main__':
    pass
    #twitter = Twitter("alatani")
    #message = "ちゅっちゅ"
    #twitter.post(message)

