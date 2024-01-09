import os
import argparse
import pyttsx3
import PyPDF2
import requests

from tqdm import tqdm

bot_token = '6668781414:AAEwBMLNtvXVlNHbyP_DPSbqW3-dqSDVreo'
chat_id = '-1002008769361'

def convert_pdf_to_voice(filename, outputname, delete_pdf):
    try:
        with open(f'{filename}.pdf', 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            text_to_read = ''

            for page_num in tqdm(range(len(pdf_reader.pages)), desc='Read Pages...'):
                page = pdf_reader.pages[page_num]
                text_to_read += page.extract_text() + ' '

            print(text_to_read)
            speaker = pyttsx3.init()

            speaker.save_to_file(text_to_read, f'{outputname}.mp3')

            speaker.runAndWait()

            speaker.stop()

            print(f'Conversion successful. MP3 file saved as {outputname}.mp3')

            if delete_pdf:
                os.remove(f'{filename}.pdf')
                print("Input PDF file has successfully been deleted!")

        return f'{filename}.pdf', f'{outputname}.mp3'

    except Exception as e:
        print(f'Error: {e}')
        return None, None

def remove_file(file_path):
    try:
        os.remove(file_path)
        print(f'File {file_path} successfully removed.')
    except FileNotFoundError:
        print(f'File {file_path} not found.')
    except Exception as e:
        print(f'Error: {e}')

def send_to_telegram(pdf_file, voice_file):

    apiURL = f'https://api.telegram.org/bot{bot_token}/sendDocument'

    try:
        with open(pdf_file, 'rb') as file:
            files = {'document': (pdf_file, file, 'application/pdf')}
            data = {'chat_id': chat_id}
            response = requests.post(apiURL, files=files, data=data)
            print(response.text)
    except Exception as e:
        print(e)


    apiURL = f'https://api.telegram.org/bot{bot_token}/sendAudio'

    try:
        with open(voice_file, 'rb') as file:
            files = {'audio': (voice_file, file, 'audio/mpeg')}
            data = {'chat_id': chat_id}
            response = requests.post(apiURL, files=files, data=data)
            print(response.text)
    except Exception as e:
        print(e)

def main():
    parser = argparse.ArgumentParser(description='PDF to Voice Converter and Telegram Sender')
    parser.add_argument('job', choices=['convert', 'remove', 'telegram'], help='Choose the job: convert, remove, or telegram')
    parser.add_argument('--filename', '-f', help='Enter PDF filename')
    parser.add_argument('--outputname', '-o', help='Enter output MP3 filename')
    parser.add_argument('--delete-pdf', action='store_true', help='Delete the input PDF file after conversion or removal')
    parser.add_argument('--file-path', '-p', help='Enter the file path for removal')

    args = parser.parse_args()

    if args.job == 'convert':
        pdf_file, voice_file = convert_pdf_to_voice(args.filename, args.outputname, args.delete_pdf)
        if pdf_file and voice_file:
            send_to_telegram(pdf_file, voice_file)
    elif args.job == 'remove':
        remove_file(args.file_path)
    elif args.job == 'telegram':
        pdf_file, voice_file = convert_pdf_to_voice(args.filename, args.outputname, args.delete_pdf)
        if pdf_file and voice_file:
            send_to_telegram(pdf_file, voice_file)

if __name__ == '__main__':
    main()
