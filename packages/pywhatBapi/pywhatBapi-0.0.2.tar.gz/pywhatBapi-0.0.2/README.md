![title](https://raw.githubusercontent.com/SaiJeevanPuchakayala/pywhatBapi/main/images/title.png)
## Project Description
pywhatBapi is a Python library for Sending whatsapp messages to many unsaved mobile numbers, using a csv file as a Database, the mobile numbers and specific messages can stored in the csv file.

## Installation
`pip install pywhatBapi`

### Usage

Import the library using the following command.

`import pywhatBapi`
1. Store all the mobile numbers and specific messages in the csv file. Format is like   ![csv_image](https://raw.githubusercontent.com/SaiJeevanPuchakayala/pywhatBapi/main/images/csv_image.png)
2. Pass the csv file name in the function `sendwhatmsgs('your_csv_filename.csv')`.
3. Then as soon as the program runs the specific message will be sent to specific number as you specified in the csv file.

### Note
As this program uses Whatsapp Api to send messages, make sure you have whatsapp desktop app on your pc and once you make whatsapp desktop app as default app in your pc to open whatsapp links  then the messages will be sent one by one automatically.

### Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
### License

MIT
