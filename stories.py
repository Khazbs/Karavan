import tornado.ioloop
import tornado.web
import json
from pymongo import MongoClient


class AdminstrationHandler(tornado.web.RequestHandler):
    def get(self):
        global settings
        cmd = self.get_argument("cmd")
        if self.get_argument("usr") != settings["remote_admin_username"] or self.get_argument("pwd") != settings["remote_admin_password"]:
            if cmd:
                self.write("Error / Ошибка")
            else:
                self.set_status(400)
                self.write("Error / Ошибка")
        else:
            if cmd not in settings["remote_admin_commands"]:
                self.write("Error / Ошибка")
            else:
                if cmd == settings["remote_admin_commands"][0]:
                    state = self.get_argument("st")
                    if state == "Yup":
                        settings["push_enabled"] = "Yup"
                        open("./settings.json", "w").write(json.dumps(settings))
                        self.write("Operation successful, my lord")
                    elif state == "Nope":
                        settings["push_enabled"] = "Nope"
                        open("./settings.json", "w").write(json.dumps(settings))
                        self.write("Operation successful, my lord")
                    else:
                        self.write("Error / Ошибка")
                elif cmd == settings["remote_admin_commands"][1]:
                    dbuser = self.get_argument("dbusr")
                    dbpassword = self.get_argument("dbpwd")
                    if dbuser and dbpassword:
                        settings["db_user"] = dbuser
                        settings["db_password"] = dbpassword
                        open("./settings.json", "w").write(json.dumps(settings))
                        global client
                        client = MongoClient(settings["connection_string"].format(dbuser=settings["db_user"],
                                                                                  dbpassword=settings["db_password"]))
                        self.write("Operation successful, my lord")
                    else:
                        self.write("Error / Ошибка")
                elif cmd == settings["remote_admin_commands"][2]:
                    state = self.get_argument("st")
                    if state == "Yup":
                        settings["pull_enabled"] = "Yup"
                        open("./settings.json", "w").write(json.dumps(settings))
                        self.write("Operation successful, my lord")
                    elif state == "Nope":
                        settings["pull_enabled"] = "Nope"
                        open("./settings.json", "w").write(json.dumps(settings))
                        self.write("Operation successful, my lord")
                    else:
                        self.write("Error / Ошибка")
                elif cmd == settings["remote_admin_commands"][3]:
                    if self.get_argument("am_I_sure") == "Yup":
                        exit(0)
                    else:
                        self.write("Error / Ошибка")


class StoriesHandler(tornado.web.RequestHandler):
    def get(self):
        if settings["pull_enabled"] != "Yup":
            self.set_status(403)
            self.render("./frontend/error.html", root_loc=settings["location"], error_title="Temporarily Disabled", error_text="Функция получения историй временно отключена администратором сервиса.")
            return
        stories = list(client[settings["db_name"]]["stories"].aggregate([{"$sample": {"size": 1}}]))
        pers = list(client[settings["db_name"]]["pers"].aggregate([{"$sample": {"size": 10}}]))
        objs = list(client[settings["db_name"]]["objs"].aggregate([{"$sample": {"size": 10}}]))
        if len(stories) < 1 or len(objs) < 10 or len(pers) < 10:
            self.set_status(500)
            self.render("./frontend/error.html", root_loc=settings["location"], error_title="Defective Database",
                        error_text="При генерации истории возникла ошибка. Скорее всего, база данных повреждена или неполноценна. Попробуйте еще раз позже.")
        else:
            story = stories[0]["value"].format(pers=pers[0]["value"], pers1=pers[1]["value"], pers2=pers[2]["value"], pers3=pers[3]["value"], pers4=pers[4]["value"],
                                 pers5=pers[5]["value"], pers6=pers[6]["value"], pers7=pers[7]["value"], pers8=pers[8]["value"], pers9=pers[9]["value"],
                                 obj=objs[0]["value"], obj1=objs[1]["value"], obj2=objs[2]["value"], obj3=objs[3]["value"], obj4=objs[4]["value"],
                                 obj5=objs[5]["value"], obj6=objs[6]["value"], obj7=objs[7]["value"], obj8=objs[8]["value"], obj9=objs[9]["value"])
            self.render("./frontend/story.html", root_loc=settings["location"], story_text=story)

    def post(self, slug):
        self.set_status(405)
        self.render("./frontend/error.html", root_loc=settings["location"], error_title="Method Not Allowed",
                    error_text="Здесь не рады POST-запросам.")


class PullHandler(tornado.web.RequestHandler):
    def get(self):
        if settings["pull_enabled"] != "Yup":
            self.set_status(403)
            self.write(json.dumps({"status": "TempDisabled"}))
            return
        stories = list(client[settings["db_name"]]["stories"].aggregate([{"$sample": {"size": 1}}]))
        pers = list(client[settings["db_name"]]["pers"].aggregate([{"$sample": {"size": 10}}]))
        objs = list(client[settings["db_name"]]["objs"].aggregate([{"$sample": {"size": 10}}]))
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
        if settings["push_enabled"] != "Yup":
            self.set_status(403)
            self.render("./frontend/error.html", root_loc=settings["location"], error_title="Temporarily Disabled", error_text="Функция добавления материалов временно отключена администратором сервиса.")
            return
        self.render("./frontend/add.html", root_loc=settings["location"])

    def post(self, slug):
        self.set_status(405)
        self.render("./frontend/error.html", root_loc=settings["location"], error_title="Method Not Allowed",
                    error_text="Здесь не рады POST-запросам.")


class ApiInfoHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./frontend/api.html", root_loc=settings["location"])

    def post(self, slug):
        self.set_status(405)
        self.render("./frontend/error.html", root_loc=settings["location"], error_title="Method Not Allowed",
                    error_text="Здесь не рады POST-запросам.")


class ApiCrapHandler(tornado.web.RequestHandler):
    def get(self, slug):
        self.set_status(404)
        self.write(json.dumps({"status": "WhereAmI?"}))

    def post(self, slug):
        self.set_status(404)
        self.write(json.dumps({"status": "WhereAmI?"}))


class PushStoriesHandler(tornado.web.RequestHandler):
    def get(self):
        if settings["push_enabled"] != "Yup":
            self.set_status(403)
            self.write(json.dumps({"status": "TempDisabled"}))
            return
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
                client[settings["db_name"]]["stories"].insert({"author": author, "value": self.get_argument("value")})
                self.write(json.dumps({"status": "Ok", "author": author, "value": text}))

    def post(self):
        if settings["push_enabled"] != "Yup":
            self.set_status(403)
            self.write(json.dumps({"status": "TempDisabled"}))
            return
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
                client[settings["db_name"]]["stories"].insert({"author": author, "value": self.get_argument("value")})
                self.write(json.dumps({"status": "Ok", "author": author, "value": text}))


class PushCharactersHandler(tornado.web.RequestHandler):
    def get(self):
        if settings["push_enabled"] != "Yup":
            self.set_status(403)
            self.write(json.dumps({"status": "TempDisabled"}))
            return
        try:
            author, text = self.get_argument("author").replace("\n", ""), self.get_argument("value").replace("\n", "")
        except tornado.web.MissingArgumentError:
            self.set_status(400)
            self.write(json.dumps({"status": "MissingArguments"}))
        else:
            client[settings["db_name"]]["pers"].insert({"author": author, "value": self.get_argument("value")})
            self.write(json.dumps({"status": "Ok", "author": author, "value": text}))

    def post(self):
        if settings["push_enabled"] != "Yup":
            self.set_status(403)
            self.write(json.dumps({"status": "TempDisabled"}))
            return
        try:
            author, text = self.get_argument("author").replace("\n", ""), self.get_argument("value").replace("\n", "")
        except tornado.web.MissingArgumentError:
            self.set_status(400)
            self.write(json.dumps({"status": "MissingArguments"}))
        else:
            client[settings["db_name"]]["pers"].insert({"author": author, "value": self.get_argument("value")})
            self.write(json.dumps({"status": "Ok", "author": author, "value": text}))


class PushObjectsHandler(tornado.web.RequestHandler):
    def get(self):
        if settings["push_enabled"] != "Yup":
            self.set_status(403)
            self.write(json.dumps({"status": "TempDisabled"}))
            return
        try:
            author, text = self.get_argument("author").replace("\n", ""), self.get_argument("value").replace("\n", "")
        except tornado.web.MissingArgumentError:
            self.set_status(400)
            self.write(json.dumps({"status": "MissingArguments"}))
        else:
            client[settings["db_name"]]["objs"].insert({"author": author, "value": self.get_argument("value")})
            self.write(json.dumps({"status": "Ok", "author": author, "value": text}))

    def post(self):
        if settings["push_enabled"] != "Yup":
            self.set_status(403)
            self.write(json.dumps({"status": "TempDisabled"}))
            return
        try:
            author, text = self.get_argument("author").replace("\n", ""), self.get_argument("value").replace("\n", "")
        except tornado.web.MissingArgumentError:
            self.set_status(400)
            self.write(json.dumps({"status": "MissingArguments"}))
        else:
            client[settings["db_name"]]["objs"].insert({"author": author, "value": self.get_argument("value")})
            self.write(json.dumps({"status": "Ok", "author": author, "value": text}))


class CrapHandler(tornado.web.RequestHandler):
    def get(self, slug):
        self.set_status(404)
        self.render("./frontend/error.html", root_loc=settings["location"], error_title="Not Found",
                    error_text="Тут ничего нет... Попробуйте воспользоваться навигационными кнопками.")

    def post(self, slug):
        self.set_status(404)
        self.render("./frontend/error.html", root_loc=settings["location"], error_title="Not Found",
                    error_text="Тут ничего нет... Попробуйте воспользоваться навигационными кнопками.")

if __name__ == "__main__":
    settings = json.loads(open("./settings.json").read())
    client = MongoClient(settings["connection_string"].format(dbuser=settings["db_user"], dbpassword=settings["db_password"]))
    app = tornado.web.Application([
        (r"/", StoriesHandler),
        (r"/administer/?", AdminstrationHandler),
        (r"/add/?", AddHandler),
        (r"/api/?", ApiInfoHandler),
        (r"/api/pull/?", PullHandler),
        (r"/api/push/stories/?", PushStoriesHandler),
        (r"/api/push/characters/?", PushCharactersHandler),
        (r"/api/push/objects/?", PushObjectsHandler),
        (r"/api/(.*)", ApiCrapHandler),
        (r'/misc/(.*)', tornado.web.StaticFileHandler, {'path': 'misc'}),
        (r'/(.*)', CrapHandler)
    ], debug=True)
    app.listen(settings["active_port"])
    tornado.ioloop.IOLoop.current().start()
