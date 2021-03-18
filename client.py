#########################################
# Niilo Liimatainen
# 16.03.2021
# Sources:
# https://docs.python.org/3/library/socketserver.html#socketserver.ThreadingMixIn
# https://docs.python.org/3/library/xmlrpc.server.html#simplexmlrpcserver-example
#########################################
import xmlrpc.client
import datetime
import json

def main():
    #Connecting to the server
    with xmlrpc.client.ServerProxy("http://127.0.0.1:8000") as proxy:
        #Proxy instance allows us to use methods from the server
        print(proxy.system.listMethods())
        print("Welcome to the online notebook!")
        while True:
            print("1) Get all topics")
            print("2) Add a new note")
            print("3) Show topic content")
            print("0) Exit")
            choice = int(input("Your choice: "))
            
            if choice == 1:
                topic_list = proxy.get_topics()
                for topic in topic_list:
                    print(topic)
                print()
            elif choice == 2:
                print(proxy.create_note(new_note()))
                print()
            elif choice == 3:
                topic = input("Give a topic: ")
                print_content(proxy.find_content(topic))
                print()
            elif choice == 0:
                print("Thank you!")
                break
            else:
                print("Invalid choice!")
                print()


#creating json from the user's note 
def new_note():
    date = str(datetime.date.today().strftime("%d/%m/%Y"))
    time = str(datetime.datetime.now().strftime("%H:%M:%S"))
    timestamp = f"{date} - {time} "
    topic = input("Give a topic: ")
    note_name = input("Note's name: ")
    text = input("Text: ")
    json_data = json.dumps({"topic": topic, "note_name": note_name, "text":text, "timestamp": timestamp})
    json_object = json.loads(json_data)
    return json_object

def print_content(json_object):
    if json_object == 0:
        print("Topic has no entries yet!")
        return
    elif json_object == -1:
        print("Error happened, try again later!") 
        return
    else:
        topic = json_object["topic"]
        note_name = json_object["note_name"]
        text = json_object["text"]
        timestamp = json_object["timestamp"]
        print(f"{topic} - {note_name}:\n   {text}\n{timestamp}")


if __name__ == "__main__":
    main()