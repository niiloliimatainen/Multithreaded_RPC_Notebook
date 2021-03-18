#########################################
# Niilo Liimatainen
# 16.03.2021
# Sources:
# https://docs.python.org/3/library/socketserver.html#socketserver.ThreadingMixIn
# https://docs.python.org/3/library/xmlrpc.server.html#simplexmlrpcserver-example
# https://docs.python.org/3/library/xml.etree.elementtree.html
#########################################
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET
import json
import socketserver
import time


# Creating threading version from the SimpleXMLRPCServer,which creates a new thread to handle each request.
class ThreadedSimpleXMLRPCServer (socketserver.ThreadingMixIn, SimpleXMLRPCServer):
    pass

#Restricting requests to a certain path
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)
 

#Creating the server
def start_server():
    with ThreadedSimpleXMLRPCServer(("127.0.0.1", 8000),
                        requestHandler=RequestHandler) as server:
        class Functions:
            def test(self):
                print("Sleeping!")
                time.sleep(20)
                print("Wake up!")
                return "Toimii"

            # Get list of topics in database
            def get_topics(self):
                root = get_root()
                topic_list = []
                if not root:
                    return "Error happened, try again later!" 
                for child in root:
                    topic_list.append(child.attrib["name"])
                return topic_list

            
            # Creates a new entry under a topic
            def create_note(self, json_object):
                root = get_root()
                if not root:
                    return "Error happened, try again later!" 

                   
                return "Note created!"

            
            # Get contents based on given topic
            def find_content(self, topic):
                root = get_root()
                if not root:
                    return -1
                for child in root:
                    if child.attrib["name"] == topic:
                        note = child.find("note")
                        note_name = note.get("name")
                        text = note.find("text").text
                        timestamp = note.find("timestamp").text
                        json_data = json.dumps({"topic": topic, "note_name": note_name, "text":text, "timestamp": timestamp})
                        json_object = json.loads(json_data)
                        return json_object
                return 0



         
        
        server.register_instance(Functions())
        server.register_introspection_functions()
        server.serve_forever()


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