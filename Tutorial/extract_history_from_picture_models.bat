@echo off
setlocal enabledelayedexpansion

:: Setze den relativen Pfad des Zielordners (dort, wo die .zip-Dateien sind)
set "folder=%~dp0picture_model\model_results"

:: Wechsle in das Verzeichnis der .zip-Dateien
cd /d "%folder%"

:: Durchlaufe alle .zip-Dateien im Ordner
for %%f in (*.zip) do (
    :: Speichern des aktuellen Dateinamens
    set "filename=%%~nf"
    
    :: Entpacken der .zip-Datei und extrahieren des PNG-Files
    echo Extrahiere %%f...
    powershell -Command "Expand-Archive -Path '%%f' -DestinationPath '!filename!'"

    :: Überprüfen, ob "model_" im Dateinamen enthalten ist
    if "!filename!" neq "!filename:model_=!" (
        :: Ersetze "model_" durch "history_" im Dateinamen
        set "newname=!filename:model_=history_!"
    ) else (
        :: Wenn "model_" nicht im Namen ist, füge "history_" vorne hinzu
        set "newname=history_!filename!"
    )

    :: Benenne die extrahierte .png Datei um
    if exist "!filename!\training_plot.png" (
        echo Umbenenne training_plot.png zu !newname!_training_plot.png
        ren "!filename!\training_plot.png" "!newname!_training_plot.png"
        
        :: Verschiebe die umbenannte PNG-Datei zurück in den Zielordner
        move "!filename!\!newname!_training_plot.png" "%folder%\!newname!_training_plot.png"
    ) else (
        echo training_plot.png nicht gefunden in %%f
    )
    
    :: Lösche das entpackte Verzeichnis
    rmdir /s /q "!filename!"
)

echo Alle Dateien wurden extrahiert, umbenannt und gespeichert.
pause


