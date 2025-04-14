import sys, os
from librosa.core import spectrum
import numpy as np
from PIL import Image
import onnxruntime
import utils
from tabulate import tabulate
import csv


class FLAD:

    def __init__(self):
        self.model_path = 'onnx/flad.onnx'
        self.img_size = 400
        self.r_map = ['FLAC', 'AAC', 'mp3', 'Opus']
        self.init_model()

    def img_preprocess(self, image_path):
        try:
            img = Image.open(image_path).resize((self.img_size, self.img_size), Image.Resampling.BICUBIC)
            img = img.convert('RGBA').convert('RGB')
        except OSError:
            print(f'\nFile broken: {image_path}')
            return None
        input_data = np.array(img).transpose(2, 0, 1)
        img_data = input_data.astype('float32')
        mean_vec = np.array([0.485, 0.456, 0.406])
        stddev_vec = np.array([0.229, 0.224, 0.225])
        norm_img_data = np.zeros(img_data.shape).astype('float32')
        for i in range(img_data.shape[0]):
            norm_img_data[i,:,:] = (img_data[i,:,:] / 255 - mean_vec[i]) / stddev_vec[i]
        norm_img_data = norm_img_data.reshape(1, 3, self.img_size, self.img_size).astype('float32')
        return norm_img_data

    def init_model(self):
        self.session_opti = onnxruntime.SessionOptions()
        self.session_opti.enable_mem_pattern = False
        self.provider = 'CPUExecutionProvider'  # or DmlExecutionProvider
        self.session = onnxruntime.InferenceSession(self.model_path, self.session_opti, providers=["CPUExecutionProvider"])
        self.session.set_providers([self.provider])
        self.model_input = self.session.get_inputs()[0].name
    
    def get_result(self, input_path, output_file='results.csv'):

        def softmax(x):
            e_x = np.exp(x - np.max(x))
            return e_x / e_x.sum(axis=0)

        # Stelle sicher, dass der Input-Pfad existiert und eine Datei oder ein Ordner ist
        if not os.path.exists(input_path):
            print(f"Fehler: Der Pfad '{input_path}' existiert nicht.")
            return

        # Wenn es sich um einen Ordner handelt, alle Audiodateien im Ordner holen
        if os.path.isdir(input_path):
            audio_files = [f for f in os.listdir(input_path) if f.endswith(('.wav', '.mp3', '.flac', '.aac', '.opus'))]
            if len(audio_files) == 0:
                print("Fehler: Keine Audiodateien im Ordner gefunden.")
                return
        else:
            # Wenn es sich um eine einzelne Datei handelt
            audio_files = [os.path.basename(input_path)]

        results = []  # Liste, um die Ergebnisse zu speichern
        correct_predictions = 0  # Zähler für richtige Vorhersagen

        # Verarbeite jede Audiodatei
        for audio_file in audio_files:
            # Wenn es sich um einen Ordner handelt, den vollen Pfad zur Datei holen
            if os.path.isdir(input_path):
                audio_path = os.path.join(input_path, audio_file)
            else:
                # Wenn es eine Datei ist, den übergebenen Pfad verwenden
                audio_path = input_path

            print(f'Verarbeite Datei: {audio_path}')
            
            print('Generate side channel...')
            y_s = utils.get_side(audio_path)
            print('Rendering spectrum...')
            utils.get_spectrum(y_s, 0, 'temp', max=20)
            spectrum_list = utils.get_file_list('temp')
            
            print('Valid samples...')
            fin = np.zeros(4)
            
            for i_idx in range(len(spectrum_list)):
                norm_img = self.img_preprocess(spectrum_list[i_idx])
                result = self.session.run([], {self.model_input: norm_img})[0][0]
                result = softmax(result)
                fin[np.argmax(result)] += 1
                print(f'Sample {i_idx+1} -> {self.r_map[np.argmax(result)]}, Prob：{np.max(result)*100:.3f}%')
            
            if fin[0] != len(spectrum_list):
                fin[0] = 0
                final_result = self.r_map[np.argmax(fin)]
            else:
                final_result = 'Lossless'

            # Bestimmen, ob die Vorhersage korrekt ist
            if 'orig-16-44-mono' in audio_file and final_result == 'Lossless':
                correctness = 'Correct'
                wrongness = ''
                correct_predictions += 1  # Erhöhe den Zähler für richtige Vorhersagen
            elif 'upscale-from-mp3-128' in audio_file and final_result != 'Lossless':
                correctness = 'Correct'
                wrongness = ''
                correct_predictions += 1  # Erhöhe den Zähler für richtige Vorhersagen
            else:
                correctness = ''
                wrongness = 'Wrong'

            # Speichere das Ergebnis in der Liste
            results.append([audio_file, final_result, correctness, wrongness])

        # Berechnung der Gesamtwahrscheinlichkeit
        total_predictions = len(results)
        accuracy = (correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0

        # Speichern der Ergebnisse als CSV-Datei
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(["Track Name", "Ergebnis", "Correctness", "Wrongness"])  # Header
            for result in results:
                writer.writerow(result)
            
            # Füge die Gesamtwahrscheinlichkeit am Ende hinzu
            writer.writerow([])
            writer.writerow([])
            writer.writerow(["Gesamtwahrscheinlichkeit aus dem Code", f"{accuracy:.2f}%"])

        print(f"\nErgebnisse wurden in '{output_file}' gespeichert. Gesammtwahrscheinlichkeit: {accuracy:.2f}%")


# Beispielaufruf
flad = FLAD()
flad.get_result(sys.argv[1], 'ergebnisse.csv')
