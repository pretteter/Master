# Anleitung zur Einrichtung und Ausführung des Projekts

Diese Anleitung erklärt, wie unter Windows mit Anaconda die benötigte Umgebung eingerichtet und das Trainingsprogramm korrekt ausgeführt wird.

---

### 🔧 1. Anaconda-Umgebung mit `.yaml`-Datei erstellen

In einer **Anaconda Prompt (CMD)** folgenden Befehl ausführen:

```bash
conda env create -f environment.yaml
```

> Sicherstellen, dass sich die Datei `environment.yaml` im aktuellen Verzeichnis befindet oder den Pfad korrekt angeben.

---

### 🚀 2. Umgebung starten

Aktivierung der Umgebung in der Anaconda Prompt:

```bash
conda activate tf
```

> `tf` sollte stimmen. Falls nicht, dann durch den Namen aus der `.yaml`-Datei ersetzen (z. B. `tf`).

---

### ⚙️ 3. NVIDIA GPU-Support aktivieren (CUDA & cuDNN installieren)

In der aktiven Umgebung ausführen:

```bash
conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1
```

> Sicherstellen, dass das System mit CUDA 11.2 kompatibel ist.

---

### 📦 4. Python-Abhängigkeiten mit `requirements.txt` installieren

In das Verzeichnis mit der Datei `requirements.txt` wechseln:

```bash
cd PFAD/ZU/requirements
```

Installation der Abhängigkeiten:

```bash
pip install -r requirements.txt
```

---

## 🧠 5. Trainings- und Testdurchlauf starten

Die relevanten Notebook-Dateien befinden sich im Unterordner:

```
./picture Model/
```

### 🔁 Trainingsdurchlauf

- Anaconda Navigator öffnen
- **Jupyter Notebook** aus der aktiven Umgebung starten
- In Jupyter `picture Model/New_Programm_audioToPicture.ipynb` öffnen
- Notebook vollständig ausführen, um das Modell zu trainieren

> Das Modell wird automatisch gespeichert und an die nächste Datei übergeben.

### 🧪 Testdurchlauf

- Nach dem Training wird automatisch `use_model_picture.ipynb` verwendet.
- In dieser Datei kann einer der drei verfügbaren Datensätze ausgewählt werden, um das trainierte Modell zu testen.
- Diese Datei kann auch komplett unabhängig verwendet werden, solange die Verzeichnisstruktur erhalten bleibt. Der Pfad zum Modell muss nur angepasst werden, genauso der Pfad zum zu testenden Datensatz

---

## 📁 Verzeichnisstruktur

```
📁 Old Stuff (hier finden sich alte Versionen des Programms)
│
📁 Final Programm/
├── 📁 picture Model/
│    ├── New_Programm_audioToPicture.ipynb
│    ├── use_model_picture.ipynb
│    ├── 📁 compare
│    │      └── (hier finden sich Vergleiche einiger Spektrogramme)
│    └── 📁 model_results
│           └── (hier befinden sich die finalen Testergebnisse)
└──📁 Unzipped_Data_Picture
        └──(hier befinden sich die originalen Datensätze)
```

## ✅ Hinweise

Falls beim Starten von Notebooks Fehler wie `No module named 'ipynb'` oder Probleme mit `numpy>=2` auftreten:
- Sicherstellen, dass die Umgebung mit den exakten Versionen erstellt wurde
- Ggf. Downgrade von numpy:

```bash
pip install numpy<2
```
