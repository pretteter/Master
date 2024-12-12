@echo off
REM Aktiviert die Conda-Umgebung (falls du eine benutzt)
call conda activate tf

REM Startet TensorBoard mit dem Log-Verzeichnis
start tensorboard --logdir=logs/hparam_tuning --host=127.0.0.1 --port=6006

REM Öffnet den Standardbrowser auf der TensorBoard-URL
start http://127.0.0.1:6006

REM Warte darauf, dass TensorBoard abgeschlossen wird
pause
