from datetime import datetime  
import json 
import base64 

MESSAGE = list()  

class Message:  
    
    def __init__(self, text, messageID, userID, tag, status) -> None:  
        self.text = text  
        self.sent_date = datetime.now()  # Call to datetime.now() should be made  
        self.messageID = messageID  
        self.userID = userID  
        self.tag = tag  
        self.answer = None
        self.end_date = None  
        self.status = status  
        # MESSAGE.append(self)  

    @property  
    def set_end_date(self):  
        self.end_date = datetime.now()  

    @classmethod  
    def create(cls, new_message):  
        data = {  
            "text": new_message.text,  
            "sent_date": str(new_message.sent_date),  # Use str directly  
            "messageID": new_message.messageID,  
            "userID": new_message.userID,  
            "tag": new_message.tag,  
            "answer" : new_message.answer,
            "end_date": str(new_message.end_date) if new_message.end_date else None,  # Check if end_date is None  
            "status": new_message.status  
        }  
        MESSAGE.append(data)
        try:  
            with open("messages.json", "r+") as file:  
                file_data = json.load(file)  
                file_data.append(data)  
                file.seek(0)  
                json.dump(file_data, file, indent=4)  
                file.truncate()  
        except FileNotFoundError:  
            with open("messages.json", "w") as file:  
                json.dump([data], file, indent=4)  

    @classmethod  
    def read_from_json(cls):
        """
        Reads messages from the JSON file and updates the MESSAGE list.
        
        Args:
            None
        
        Returns:
            None
        """
        try:
            with open('messages.json', 'r') as file:
                file_data = json.load(file)
                MESSAGE.clear()
                for message in file_data:
                    MESSAGE.append(message)
        except FileNotFoundError:
            pass
    @classmethod
    def update_message(cls, message_id, new_data):
        """Updates a message in the database."""
        # Read the existing data from the JSON file
        with open('messages.json', 'r') as f:
            messages = json.load(f)

        # Find the message to update
        for i, message in enumerate(messages):
            if message['messageID'] == message_id:
                # Update the message data
                messages[i] = new_data
                break
        else:
            raise ValueError(f"Message with ID {message_id} not found")

        # Write the updated data back to the JSON file
        with open('messages.json', 'w') as f:
            json.dump(messages, f, indent=4)
    @classmethod  
    def delete(cls, messageID):  
        """  
        Deletes a message from the MESSAGE list.  
        """  
        for message in MESSAGE:  
            if message.messageID == messageID:  # Use messageID not id  
                MESSAGE.remove(message)  
                break  
        cls.write_all()  

    @classmethod  
    def write_all(cls):  
        """  
        Writes the MESSAGE list to the JSON file.  
        """  
        messages = [message.__dict__ for message in MESSAGE]  # Create list of message dictionaries  
        with open('messages.json', 'w') as f:  
            
            json.dump(messages, f, indent=4)  # Format the JSON output nicely  

    

    @classmethod  
    def find_by_messageID(cls, MiD):  
        """  
        Finds a message by its text and tag.  

        Args:  
            text (str): The text of the message.  
            tag (str): The tag of the message.  

        Returns:  
            Message: The message object if found, None otherwise.  
        """  
        print(MiD)  
        for message in MESSAGE:  
            # print(message['text'] , message['tag'])
            if message['messageID'] == MiD : 
                print("suc")
                return message  # Return the Message object if found  
        return None  
    
    @classmethod
    def find_user_messages (cls, MiD):  
          
        messages = list()
        userId = 0
        # message = Message.find_by_messageID(MiD)
        for message in MESSAGE:  
            # print(message['text'] , message['tag'])
            if message['messageID'] == MiD : 
                userId = message['userID'] 
        for message in MESSAGE:
            if message["userID"] == userId:
                messages.append(message)

        return messages
    @classmethod
    async def find_by_status(cls, status) :
        with open('messages.json', 'r') as f:
            messages = json.load(f)

        return [message for message in messages if message['status'] == status]
# if __name__ == '__main__':  
#     # m1 = Message("hello", 1, 2, 3, 7)  
#     Message.read_from_json()
#     print(*MESSAGE)
#     # m = Message.find_by_messageID(930)
#     # print(m["userID"])