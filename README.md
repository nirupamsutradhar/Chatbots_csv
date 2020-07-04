# chatbot_demo

A ChatBot Widget stores the data in the CSV files.
## How to use:
* Clone the repo
* open the terminal in the project directory and run the below commands
    - rasa train
    - Once the bot has been trained, run the bot using the below commands
    - rasa run actions
    - rasa run -m models --enable-api --cors "*" --debug 
* the entered data is stored in datafile.csv