#########################################
# Niilo Liimatainen
# 16.03.2021
# Sources:
# https://docs.python.org/3/library/socketserver.html#socketserver.ThreadingMixIn
# https://docs.python.org/3/library/xmlrpc.server.html#simplexmlrpcserver-example
# https://docs.python.org/3/library/xml.etree.elementtree.html
# https://requests.readthedocs.io/en/master/
#########################################
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET
import json
import socketserver
import time
import requests

 
# Creating threading version from the SimpleXMLRPCServer, which creates a new thread to handle each request.
class ThreadedSimpleXMLRPCServer (socketserver.ThreadingMixIn, SimpleXMLRPCServer):
    pass

#Restricting requests to a certain path
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)
 

#Creating the server
def start_server():
    try:
        server = ThreadedSimpleXMLRPCServer(("127.0.0.1", 8000), requestHandler=RequestHandler)
        class Functions:
            # Get list of topics in the database
            def get_topics(self):
                root = get_root()
                topic_list = []
                if not root:
                    return "Error happened, try again later!" 
                for child in root:
                    topic_list.append(child.attrib["name"])
                return topic_list

            
            # Creates a new entry under a topic. Wikipedia query or user made note.
            def create_note(self, json_object):
                try:
                    tree = ET.parse("db.xml")
                    root = tree.getroot()
                    topic_exists = 0
                    for child in root:
                        # Find out if topic already exists
                        if child.attrib["name"] == json_object["topic"]:
                            # Find out if note name is already taken
                            for note in child.findall("note"):
                                if note.get("name") == json_object["note_name"]:
                                    return "Note's name is already taken!"
                            new_note = ET.SubElement(child, "note")
                            new_note.set("name", json_object["note_name"])
                            topic_exists = 1
                    # If new topic, create it
                    if not topic_exists:
                        new_topic = ET.SubElement(root, "topic")
                        new_topic.set("name", json_object["topic"]) 
                        new_note = ET.SubElement(new_topic, "note")
                        new_note.set("name", json_object["note_name"])

                    text = ET.SubElement(new_note, "text")
                    text.text = json_object["text"]
                    timestamp = ET.SubElement(new_note, "timestamp")
                    timestamp.text = json_object["timestamp"]
                    tree.write("db.xml")
                    return "Note created!"
                except:
                    return "Error happened, try again later!"

            
            # Get contents based on given topic
            def find_content(self, topic):
                root = get_root()
                content_list = []
                if not root:
                    return -1
                for child in root:
                    if child.attrib["name"] == topic:
                        for note in child.findall("note"):
                            note_name = note.get("name")
                            text = note.find("text").text
                            timestamp = note.find("timestamp").text
                            json_data = json.dumps({"topic": topic, "note_name": note_name, "text":text, "timestamp": timestamp})
                            json_object = json.loads(json_data)
                            content_list.append(json_object)
                        return content_list
                return 0


            # Finding relevant Wikipedia pages from user's search terms and returning their links
            def query_wikipedia(self, search_terms):
                try:
                    URL = "https://en.wikipedia.org/w/api.php"
                    PARAMS = {
                        "action": "opensearch",
                        "search": search_terms,
                        "limit": "3"
                    }
                    r = requests.get(url=URL, params=PARAMS)
                    data = r.json()
                    data = f"Page titles and links:\n   {data[1]}\n   {data[3]}"
                    return data
                except:
                    return "Error happened, try again later!"


        server.register_instance(Functions())
        server.serve_forever()
    except:
        print("Error happened in maintaining the server!")


#Helper function to get the root from the XML tree
def get_root():
    try:
        root = ET.parse("db.xml").getroot()
    except:
        print("Exception happend with database!")
        return 0
    return root


if __name__ == "__main__":
    start_server()