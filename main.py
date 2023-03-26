import openai
#from flask import Flask, request, render_template
import tkinter as tk
import textwrap

openai.api_key = "YOUR API KEY"
#app = Flask(__name__)

class ChatBotGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Homemade GPT")
        self.master.geometry("1000x900")
        self.messages = []

        # Set program icon
        icon_path = "Girl.ico"  # Replace with the actual path to your icon file
        self.master.iconbitmap(icon_path)

        # Set background color
        self.master.config(bg="#101010")

        # Calculate the window dimensions and offsets
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = 1000
        window_height = 900
        x_offset = (screen_width - window_width) // 2
        y_offset = (screen_height - window_height) // 2

        # Set the window dimensions and offsets
        self.master.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")

        # Create chat history display area
        self.chat_history = tk.Text(master, bg="#333333", fg="#fff", font=("Helvetica", 15), state="disabled")
        self.chat_history.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Create message input area with scrollbar
        self.message_input_scrollbar = tk.Scrollbar(master)
        self.message_input_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.message_input = tk.Text(master, bg="#1C1C1C", fg="#fff", font=("Helvetica", 16), height=3, yscrollcommand=self.message_input_scrollbar.set)
        self.message_input.config(insertbackground='white')
        self.message_input.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.message_input_scrollbar.config(command=self.message_input.yview)

        # Create send button
        self.send_button = tk.Button(master, text="Send", bg="#006666", fg="#fff", font=("Helvetica", 14), command=self.send_message)
        self.send_button.pack(pady=10, padx=10, fill=tk.BOTH)

        # Bind Enter key to send button
        self.message_input.bind("<Return>", lambda event: self.send_button.invoke())

        # Bind Shift+Enter key to create a new line in the input area
        self.shift_enter_count = 0
        self.message_input.bind("<Shift-Return>", lambda event: self.insert_newline())

        # Greet user
        self.add_system_message("Hi, how can I help you today?")

    def insert_newline(self):
        # Get the current cursor position
        cursor_pos = self.message_input.index(tk.INSERT)

        # Set focus to message input area
        self.message_input.focus()

        # Insert a space character if shift+enter has been pressed
        self.message_input.insert(cursor_pos, "")

        # Reset the counter for Shift+Enter key presses
        self.reset_shift_enter_count()

    def reset_shift_enter_count(self):
        # Reset the counter for Shift+Enter key presses
        self.shift_enter_count = 0

    def add_user_message(self, message):
        self.messages.append({"role": "user", "content": message})
        self.display_message("You", message)

    def add_system_message(self, message):
        self.messages.append({"role": "system", "content": message})
        self.display_message("System", message)

    def add_bot_message(self, message):
        self.messages.append({"role": "bot", "content": message})
        self.display_message("Besty", message)

    def display_message(self, sender, message):
        self.chat_history.config(state="normal")
        wrapped_message = "\n".join(textwrap.wrap(message, width=100))
        if sender == "You":
            self.chat_history.insert(tk.END, f"{sender}: {wrapped_message}\n")
        elif sender == "System":
            self.chat_history.insert(tk.END, f"{sender}: {wrapped_message}\n", "system_message")
        else:
            self.chat_history.insert(tk.END, f"{sender}: {wrapped_message}\n\n")
        self.chat_history.config(state="disabled")
        self.chat_history.see(tk.END)

        # configure tag for system messages
        self.chat_history.tag_config("system_message", foreground="#48BF91")

    def send_message(self):
        user_message = self.message_input.get("1.0", tk.END).strip()
        self.add_user_message(user_message)
        self.message_input.delete("1.0", tk.END)

        # Build prompt using previous messages
        prompt = ""
        for message in self.messages:
            if message["role"] == "user":
                prompt += f"\nYou: {message['content']}\n"
            elif message["role"] == "bot":
                prompt += f"\nBot: {message['content']}\n"
        prompt += f"\nYou: {user_message}\nBot:"

        # Generate response using GPT-3.5
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=2048,
            n=1,
            stop=None,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Get the bot response
        bot_message = response.choices[0].text.strip()

        # Split the response into chunks of 2000 characters or less
        chunks = [bot_message[i:i + 2000] for i in range(0, len(bot_message), 2000)]


        # Add each chunk as a separate system message
        for i, chunk in enumerate(chunks):
            if i == 0:
                self.add_bot_message(chunk)
            else:
                self.add_system_message(chunk)


#if __name__ == '__main__':
    #app.run(debug=True)


root = tk.Tk()
ChatBotGUI(root)
root.mainloop()