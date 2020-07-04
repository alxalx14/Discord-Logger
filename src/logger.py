import ujson

from requests import get
from os import path, mkdir

IMAGE_EXTENSIONS = ["png", "jpg", "jfif", "jpeg", "gif"]
OTHER_EXTENSIONS = {
    "exe": "PE Files",
    "json": "JSON Files",
    "xml": "XML Files",
    "txt": "Text Files",
    "log": "Log Files",
    "py": "Python Files",
    "c": "C Files",
    "cs": "C# Files",
    "cpp": "C++ Files",
    "torrent": "Torrent Files"
}


def checkExistence(folder_path: str) -> bool:
    """
    Checks if the guild ID
    folder already exists.
    Will return True/False
    depending on the result.
    :return:
    """
    if path.isdir(folder_path):
        return True
    return False


class logger:
    def __init__(self, message: dict, id_key: str):
        """
        This is the constructor
        for the logging class.
        :param message
        """
        self.guild_id = message[id_key]["guild"]["id"]
        self.channel_id = message[id_key]["guild"]["channel"]["id"]
        self.guild_type = message[id_key]["message"]["type"]
        self.id_key = id_key
        self.message = message

    def saveToJSON(self, path_to_save: str, path_exists: bool) -> None:
        """
        This Function will save the
        message and its contents to
        a JSON file, if the file
        already exists, but needs to
        be appended new info, then
        it will read and rewrite the data
        :param path_exists:
        :param path_to_save:
        :return:
        """
        new_message = {}
        if path_exists:
            try:
                with open(path_to_save, "r", encoding="utf-8") as old_file:
                    old_data = ujson.loads(old_file.read())
                for _messageID in old_data:
                    new_message[_messageID] = old_data[_messageID]
            except ValueError:
                pass
        new_message[self.id_key] = self.message[self.id_key]

        with open(path_to_save, "w", encoding="utf-8") as log_file:
            log_file.write(ujson.dumps(new_message, indent=8, ensure_ascii=False))

    def saveDM(self):
        """
        Used to log messages sent in
        DMs(Private messages), identified
        by channel ID.
        :return:
        """
        file_location = "logs/DM/%s.json" % self.channel_id
        self.saveToJSON(
            file_location,
            path.isfile(file_location)
        )

    def saveGroup(self):
        """
        Used to save messages from
        DM groups, identified by
        channel ID.
        :return:
        """
        file_location = "logs/Group DM/%s.json" % self.channel_id
        self.saveToJSON(
            file_location,
            path.isfile(file_location)
        )

    def saveServer(self):
        """
        Used to save messages from
        guilds, stores in specific
        Folder identified by Guild ID.
        :return:
        """
        dir_location = "logs/Servers/%s" % self.guild_id
        file_location = "%s/%s.json" % (
            dir_location,
            self.channel_id)
        if not path.isdir(dir_location):
            mkdir(dir_location)
        self.saveToJSON(
            file_location,
            path.isfile(file_location)
        )

    def saveFile(self):
        """
        We sent a simple GET request
        to the file url, and then
        proceed to store the file
        and also store its path in
        the JSON data. Supports all
        type of files, without risking
        arbitrary code execution.
        :return:
        """
        try:
            url = self.message[self.id_key]["message"]["content"]
            file = url.split("/")[-1]
            file_type = file.split(".")[1]
            file_type = "Images" if file_type in IMAGE_EXTENSIONS else OTHER_EXTENSIONS.get(file_type, "Others")
            file_path = "logs/Files/%s/%s" % (file_type, file)
            data = get(url, stream=True)
            with open(file_path, "wb") as f:
                for chunk in data:
                    f.write(chunk)
            self.message[self.id_key]["message"]["path_to_file"] = str(file_path)
        except:
            pass

    def save(self, has_file: bool):
        """
        Called by main program to save
        message, has a dictionary with
        the channel type to store the
        message accordingly.
        :param has_file:
        :return:
        """
        if has_file:
            self.saveFile()

        return {
            "text": self.saveServer,
            "private": self.saveDM,
            "group": self.saveGroup
        }.get(self.guild_type, None)()
