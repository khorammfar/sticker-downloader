import cv2
import pyrogram
from PIL import Image, UnidentifiedImageError
import os

class Client(pyrogram.Client):
    
    def __init__(self):
        self.API_KEY = (15191079, '315b102a75e9382be971f4b26dbef6f4',)
        self.API_TOKEN = "1720394991:AAE_BtVNLDe46rYKwLcgyR5RA96J9mGv7MY"
        self.PROXY = dict(scheme="http", hostname="127.0.0.1", port=8118)
        
        super(Client, self).__init__(
            "conf/auth",
            *self.API_KEY,
            bot_token=self.API_TOKEN,
            proxy=self.PROXY
        )
    
        self.add_handler(
            pyrogram.handlers.MessageHandler(
                self.on_convert,
                filters=pyrogram.filters.sticker|pyrogram.filters.animation
            )
        )
        
        if not os.path.exists('temp'):
            os.mkdir('temp')

        self.run()

    def on_convert(self, client:pyrogram.Client, message:pyrogram.types.Message):
        sent = message.reply('**Downloading ...**', quote=True)

        document:str = message.download()
        
        sent.edit('**Converting ... **')

        image_path:str = "temp/" + (message.sticker or message.animation).file_id + ".jpg"
        
        sent.edit('**Converting ... [1]**') 
        
        if not self.convert(
            document=document,
            output_path=image_path
        ):
            return sent.edit('__Sorry, we cannot convert this.__')

        sent.edit('**Uploading...**')
        
        photo_sent = message.reply_photo(image_path, quote=True)
        photo_sent.reply_document(image_path, quote=True)
        
        sent.delete()
        
        message.reply('**Here you are!**')

    def convert(self, document, output_path):
        try:
            image:Image = Image.open(document).convert('RGB')
        except UnidentifiedImageError:
            try:
                videocapture = cv2.VideoCapture(document)
                cv2.imwrite(output_path, videocapture.read()[-1])
                videocapture.release()
                cv2.destroyAllWindows()
                return True
            except cv2.error:
                ...
        else:
            image.save(output_path, "jpeg")
            return True

Client()