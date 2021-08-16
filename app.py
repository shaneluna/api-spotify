from flask import Flask
from flask_restful import Api, Resource
from api.SpotifyAPI import SpotifyAPI
import config

app = Flask(__name__)
api = Api(app)
spotify = SpotifyAPI(config.CLIENT_ID, config.CLIENT_SECRET)

class SearchList(Resource):
    def get(self, query):
        return spotify.search(query)
api.add_resource(SearchList, "/search/<string:query>")

class SearchAlbumList(Resource):
   def get(self, query):
      return spotify.search_album(query)
api.add_resource(SearchAlbumList, "/search/album/<string:query>")

class SearchArtistList(Resource):
   def get(self, query):
      return spotify.search_artist(query)
api.add_resource(SearchArtistList, "/search/artist/<string:query>")

class SearchPlaylistList(Resource):
   def get(self, query):
      return spotify.search_playlist(query)
api.add_resource(SearchPlaylistList, "/search/playlist/<string:query>")

class SearchTrackList(Resource):
   def get(self, query):
      return spotify.search_track(query)
api.add_resource(SearchTrackList, "/search/track/<string:query>")

class SearchShowList(Resource):
   def get(self, query):
      return spotify.search_show(query)
api.add_resource(SearchShowList, "/search/show/<string:query>")

class SearchEpisodeList(Resource):
   def get(self, query):
      return spotify.search_episode(query)
api.add_resource(SearchEpisodeList, "/search/episode/<string:query>")

if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0')