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
    # Connecting to the server
    try:
        # Proxy instance allows us to use methods from the server
        proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:8000")
        print("Welcome to the online notebook!")
        while True:
            print("1) Get all topics")
            print("2) Add a new note")
            print("3) Show topic content")
            print("4) Find additional information from Wikipedia")
            print("0) Exit")
            choice = int(input("Your choice: "))
            
            if choice == 1:
                topic_list = proxy.get_topics()
                for topic in topic_list:
                    print(topic)
                print()
            elif choice == 2:
                print(proxy.create_note(new_note(1, None)))
                print()
            elif choice == 3:
                topic = input("Give a topic: ")
                print_content(proxy.find_content(topic))
            elif choice == 4:
                search_terms = input("Name the search terms: ")
                info = proxy.query_wikipedia(search_terms)
                print(info)
                answer = input("Do you want to append these links under a topic (y/n)?")
                if answer == "y":
                    print(proxy.create_note(new_note(0, info)))
                print()
            elif choice == 0:
                print("Thank you!")
                break
            else:
                print("Invalid choice!")
                print()
    except:
        print("Can't connect to the server!")


# Creating json from the user's note. Flag tells if the user is appending topic with Wikipedia query or creating a new note. 
def new_note(flag, info):
    date = str(datetime.date.today().strftime("%d/%m/%Y"))
    time = str(datetime.datetime.now().strftime("%H:%M:%S"))
    timestamp = f"{date} - {time} "
    topic = input("Give a topic: ")
    note_name = input("Note's name: ")
    if flag:
        text = input("Text: ")
    else:
        text = info
    json_data = json.dumps({"topic": topic, "note_name": note_name, "text":text, "timestamp": timestamp})
    json_object = json.loads(json_data)
    return json_object

# Printing the content from a certain topic
def print_content(content_list):
    if content_list == 0:
        print("Topic has no entries yet!\n")
        return
    elif content_list == -1:
        print("Error happened, try again later!") 
        return
    else:
        for json_object in content_list:
            topic = json_object["topic"]
            note_name = json_object["note_name"]
            text = json_object["text"]
            timestamp = json_object["timestamp"]
            print(f"{topic} - {note_name}:\n   {text}\n{timestamp}\n")


if __name__ == "__main__":
    main()