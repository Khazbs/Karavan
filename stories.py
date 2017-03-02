import tornado.ioloop
import tornado.web
import json
from pymongo import MongoClient

location = "insert_root_location_here"  # Например, http://roctbb.net:1337
client = MongoClient("insert_connection_string_here")


class StoriesHandler(tornado.web.RequestHandler):
    def get(self):
        stories = list(client["karavan_stories"]["stories"].aggregate([{"$sample": {"size": 1}}]))
        pers = list(client["karavan_stories"]["pers"].aggregate([{"$sample": {"size": 10}}]))
        objs = list(client["karavan_stories"]["objs"].aggregate([{"$sample": {"size": 10}}]))
        if len(stories) < 1 or len(objs) < 10 or len(pers) < 10:
            self.set_status(500)
            self.render("./frontend/error.html", root_loc=location, error_title="Defective Database",
                        error_text="При генерации истории возникла ошибка. Скорее всего, база данных повреждена или неполноценна. Попробуйте еще раз позднее.")
        else:
            story = stories[0]["value"].format(pers=pers[0]["value"], pers1=pers[1]["value"], pers2=pers[2]["value"], pers3=pers[3]["value"], pers4=pers[4]["value"],
                                 pers5=pers[5]["value"], pers6=pers[6]["value"], pers7=pers[7]["value"], pers8=pers[8]["value"], pers9=pers[9]["value"],
                                 obj=objs[0]["value"], obj1=objs[1]["value"], obj2=objs[2]["value"], obj3=objs[3]["value"], obj4=objs[4]["value"],
                                 obj5=objs[5]["value"], obj6=objs[6]["value"], obj7=objs[7]["value"], obj8=objs[8]["value"], obj9=objs[9]["value"])
            self.render("./frontend/story.html", root_loc=location, story_text=story)

    def post(self, slug):
        self.set_status(405)
        self.render("./frontend/error.html", root_loc=location, error_title="Method Not Allowed",
                    error_text="Здесь не рады POST-запросам.")


class PullHandler(tornado.web.RequestHandler):
    def get(self):
        stories = list(client["karavan_stories"]["stories"].aggregate([{"$sample": {"size": 1}}]))
        pers = list(client["karavan_stories"]["pers"].aggregate([{"$sample": {"size": 10}}]))
        objs = list(client["karavan_stories"]["objs"].aggregate([{"$sample": {"size": 10}}]))
        if len(stories) < 1 or len(objs) < 10 or len(pers) < 10:
            self.set_status(500)
            self.write(json.dumps({"status": "DefectiveDatabase"}))
        else:
            story = stories[0]["value"].format(pers=pers[0]["value"], pers1=pers[1]["value"], pers2=pers[2]["value"], pers3=pers[3]["value"], pers4=pers[4]["value"],
                                 pers5=pers[5]["value"], pers6=pers[6]["value"], pers7=pers[7]["value"], pers8=pers[8]["value"], pers9=pers[9]["value"],
                                 obj=objs[0]["value"], obj1=objs[1]["value"], obj2=objs[2]["value"], obj3=objs[3]["value"], obj4=objs[4]["value"],
                                 obj5=objs[5]["value"], obj6=objs[6]["value"], obj7=objs[7]["value"], obj8=objs[8]["value"], obj9=objs[9]["value"])
            self.write(json.dumps({"status": "Ok", "text": story}))


class AddHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./frontend/add.html", root_loc=location)

    def post(self, slug):
        self.set_status(405)
        self.render("./frontend/error.html", root_loc=location, error_title="Method Not Allowed",
                    error_text="Здесь не рады POST-запросам.")


class ApiInfoHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./frontend/api.html", root_loc=location)

    def post(self, slug):
        self.set_status(405)
        self.render("./frontend/error.html", root_loc=location, error_title="Method Not Allowed",
                    error_text="Здесь не рады POST-запросам.")


class ApiCrapHandler(tornado.web.RequestHandler):
    def get(self, slug):
        self.set_status(404)
        self.write(json.dumps({"status": "WhereAmI?"}))

    def post(self, slug):
        self.set_status(404)
        self.write(json.dumps({"status": "WhereAmI?"}))


class ApiPushStoriesHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            author, text = self.get_argument("author").replace("\n", ""), self.get_argument("value").replace("\n", "")
        except tornado.web.MissingArgumentError:
            self.set_status(400)
            self.write(json.dumps({"status": "MissingArguments"}))
        else:
            try:
                text.format(pers="test", pers1="test", pers2="test", pers3="test", pers4="test",
                            pers5="test", pers6="test", pers7="test", pers8="test", pers9="test",
                            obj="test", obj1="test", obj2="test", obj3="test", obj4="test",
                            obj5="test", obj6="test", obj7="test", obj8="test", obj9="test")
            except KeyError:
                self.set_status(422)
                self.write(json.dumps({"status": "BadTemplate"}))
            else:
                client["karavan_stories"]["stories"].insert({"author": author, "value": self.get_argument("value")})
                self.write(json.dumps({"status": "Ok", "author": author, "value": text}))

    def post(self):
        try:
            author, text = self.get_argument("author").replace("\n", ""), self.get_argument("value").replace("\n", "")
        except tornado.web.MissingArgumentError:
            self.set_status(400)
            self.write(json.dumps({"status": "MissingArguments"}))
        else:
            try:
                text.format(pers="test", pers1="test", pers2="test", pers3="test", pers4="test",
                            pers5="test", pers6="test", pers7="test", pers8="test", pers9="test",
                            obj="test", obj1="test", obj2="test", obj3="test", obj4="test",
                            obj5="test", obj6="test", obj7="test", obj8="test", obj9="test")
            except KeyError:
                self.set_status(422)
                self.write(json.dumps({"status": "BadTemplate"}))
            else:
                client["karavan_stories"]["stories"].insert({"author": author, "value": self.get_argument("value")})
                self.write(json.dumps({"status": "Ok", "author": author, "value": text}))


class ApiPushCharactersHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            author, text = self.get_argument("author").replace("\n", ""), self.get_argument("value").replace("\n", "")
        except tornado.web.MissingArgumentError:
            self.set_status(400)
            self.write(json.dumps({"status": "MissingArguments"}))
        else:
            client["karavan_stories"]["pers"].insert({"author": author, "value": self.get_argument("value")})
            self.write(json.dumps({"status": "Ok", "author": author, "value": text}))

    def post(self):
        try:
            author, text = self.get_argument("author").replace("\n", ""), self.get_argument("value").replace("\n", "")
        except tornado.web.MissingArgumentError:
            self.set_status(400)
            self.write(json.dumps({"status": "MissingArguments"}))
        else:
            client["karavan_stories"]["pers"].insert({"author": author, "value": self.get_argument("value")})
            self.write(json.dumps({"status": "Ok", "author": author, "value": text}))


class ApiPushObjectsHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            author, text = self.get_argument("author").replace("\n", ""), self.get_argument("value").replace("\n", "")
        except tornado.web.MissingArgumentError:
            self.set_status(400)
            self.write(json.dumps({"status": "MissingArguments"}))
        else:
            client["karavan_stories"]["objs"].insert({"author": author, "value": self.get_argument("value")})
            self.write(json.dumps({"status": "Ok", "author": author, "value": text}))

    def post(self):
        try:
            author, text = self.get_argument("author").replace("\n", ""), self.get_argument("value").replace("\n", "")
        except tornado.web.MissingArgumentError:
            self.set_status(400)
            self.write(json.dumps({"status": "MissingArguments"}))
        else:
            client["karavan_stories"]["objs"].insert({"author": author, "value": self.get_argument("value")})
            self.write(json.dumps({"status": "Ok", "author": author, "value": text}))


class CrapHandler(tornado.web.RequestHandler):
    def get(self, slug):
        self.set_status(404)
        self.render("./frontend/error.html", root_loc=location, error_title="Not Found",
                    error_text="Тут ничего нет... Попробуйте воспользоваться навигационными кнопками.")
    def post(self, slug):
        self.set_status(404)
        self.render("./frontend/error.html", root_loc=location, error_title="Not Found",
                    error_text="Тут ничего нет... Попробуйте воспользоваться навигационными кнопками.")

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", StoriesHandler),
        (r"/add/?", AddHandler),
        (r"/api/?", ApiInfoHandler),
        (r"/api/pull/?", PullHandler),
        (r"/api/push/stories/?", ApiPushStoriesHandler),
        (r"/api/push/characters/?", ApiPushCharactersHandler),
        (r"/api/push/objects/?", ApiPushObjectsHandler),
        (r"/api/(.*)", ApiCrapHandler),
        (r'/misc/(.*)', tornado.web.StaticFileHandler, {'path': 'misc'}),
        (r'/(.*)', CrapHandler)
    ], debug=True)
    app.listen(1337)
    tornado.ioloop.IOLoop.current().start()
