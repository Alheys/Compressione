import os
import gzip
import bz2
import lzma
import zipfile
import time

def compressione_gzip(percorso_input, cartella_output, livello):
    file_output = os.path.join(cartella_output, f"gzip_{livello}.gz")
    tempo_inizio = time.time()
    with open(percorso_input, 'rb') as file_in:
        with gzip.open(file_output, 'wb', compresslevel=livello) as file_out:
            file_out.writelines(file_in)
    durata = time.time() - tempo_inizio
    return file_output, durata

def compressione_bzip2(percorso_input, cartella_output, livello):
    file_output = os.path.join(cartella_output, f"bzip2_{livello}.bz2")
    tempo_inizio = time.time()
    with open(percorso_input, 'rb') as file_in:
        with bz2.BZ2File(file_output, 'wb', compresslevel=livello) as file_out:
            file_out.writelines(file_in)
    durata = time.time() - tempo_inizio
    return file_output, durata

def compressione_xz(percorso_input, cartella_output, livello):
    file_output = os.path.join(cartella_output, f"xz_{livello}.xz")
    tempo_inizio = time.time()
    with open(percorso_input, 'rb') as file_in:
        with lzma.open(file_output, 'wb', preset=livello) as file_out:
            file_out.writelines(file_in)
    durata = time.time() - tempo_inizio
    return file_output, durata

def compressione_zip(percorso_input, cartella_output):
    file_output = os.path.join(cartella_output, "zip.zip")
    tempo_inizio = time.time()
    with zipfile.ZipFile(file_output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zip_f:
        zip_f.write(percorso_input, os.path.basename(percorso_input))
    durata = time.time() - tempo_inizio
    return file_output, durata

def log_compressione(file_log, metodo, livello, dimensione_input, dimensione_output, durata):
    rapporto = (dimensione_output / dimensione_input) * 100  
    riduzione_percentuale = 100 - rapporto  
    riduzione_dimensione = dimensione_input - dimensione_output 
    with open(file_log, 'a') as log:
        log.write(f"Metodo: {metodo}, Livello: {livello}, Tempo: {durata:.4f} sec, Dimensione: {dimensione_output} byte, Rapporto: {rapporto:.2f}%%, Ridotto: {riduzione_percentuale:.2f}%% ({riduzione_dimensione} byte)\n")

def main():
    percorso_input = input("Inserisci il percorso del file da comprimere: ").strip()
    if not os.path.isfile(percorso_input):
        print("Percorso file non valido.")
        return

    dimensione_input = os.path.getsize(percorso_input)
    cartella_output = os.path.dirname(percorso_input)
    file_log = os.path.join(cartella_output, "log_compressione.txt")
    livelli_compressione = [1, 5, 9]


    with open(file_log, 'w') as log:

        for livello in livelli_compressione:
            # Compressione Gzip
            file_gzip, tempo_gzip = compressione_gzip(percorso_input, cartella_output, livello)
            dimensione_gzip = os.path.getsize(file_gzip)
            log_compressione(file_log, "gzip", livello, dimensione_input, dimensione_gzip, tempo_gzip)

            # Compressione Bzip2
            file_bzip2, tempo_bzip2 = compressione_bzip2(percorso_input, cartella_output, livello)
            dimensione_bzip2 = os.path.getsize(file_bzip2)
            log_compressione(file_log, "bzip2", livello, dimensione_input, dimensione_bzip2, tempo_bzip2)

            # Compressione Xz
            file_xz, tempo_xz = compressione_xz(percorso_input, cartella_output, livello)
            dimensione_xz = os.path.getsize(file_xz)
            log_compressione(file_log, "xz", livello, dimensione_input, dimensione_xz, tempo_xz)

        # Compressione Zip
        file_zip, tempo_zip = compressione_zip(percorso_input, cartella_output)
        dimensione_zip = os.path.getsize(file_zip)
        log_compressione(file_log, "zip", 9, dimensione_input, dimensione_zip, tempo_zip)

        print(f"Compressione completata. Registro scritto in {file_log}")

if __name__ == "__main__":
    main()

