# HomeGPT-Chatbot
*By Bamboothesecond

*This is a Python program for a Chatbot GUI created using the OpenAI's latest engine which is davinci-003. It allows users to input messages and receive responses from the Chatbot in a Graphical User Interface (GUI) format.

The program creates a window using tkinter and sets its dimensions, background color, and icon. The Chatbot GUI is made up of a chat history display area, message input area with scrollbar, and a send button. The program also allows users to press Enter or Shift + Enter to send messages.

The Chatbot GUI has three functions to add messages to the GUI for the user, the system, and the Chatbot. The display_message() function formats the messages and adds them to the chat history display area.

The send_message() function takes the user input, adds it to the chat history display area, builds a prompt using previous messages, and generates a response using the OpenAI's davinci-003 engine. Finally, it adds the Chatbot response to the chat history display area.

Overall, this program is a basic implementation of a Chatbot GUI using OpenAI's davinci-003 engine.
