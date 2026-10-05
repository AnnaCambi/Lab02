def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    try:   #apro il file in modalità lettura, gestendo le eccezioni
        album = {} #creo l'album in cui andrò a inserire le foto
        with open(file_path, 'r', encoding='utf-8') as file:
            riga = file.readline()  #leggo la prima riga in modo da saltare l'intestazione del file
            for line in file:
                riga = line.strip().split(',')
                mese = int(riga[3])
                anno = int(riga[4])  #estraggo e converto in interi il mese e l'anno
                foto = {
                    'codice' : riga[0],
                    'titolo' : riga[1],
                    'autore' :  riga[2],
                    'mese' : mese,
                    'anno' :  anno,
                }  #salvo le foto singolarmente in un dizionario

                if anno not in album:
                    album[anno] = []      #se l'anno non è presente nell'album lo aggiungo

                album[anno].append(foto)  #aggiungo le foto all'album dell'anno

        return album

    except FileNotFoundError:
        print('File non trovato')
        return None #se il file non viene trovato, stampo il problema e non faccio uscire nulla dalla funzione


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    if 1 <= mese <= 12:    #controllo che il mese esista
        pass
    else:
        return None

    if cerca_foto(album, codice) is not None: #controllo che la foto non sia già presente negli album
        return None

    foto = {
        'codice': codice,
        'titolo': titolo,
        'autore': autore,
        'mese': mese,
        'anno': anno,
    } #salvo la foto in un dizionario
    try:
        with open(file_path, 'a', encoding='utf-8') as file: #apro il file in modalità append, gestendo le eccezioni
            file.write(f"\n{codice},{titolo},{autore},{mese},{anno}") #inserisco la nuova foto nel formato corretto
    except FileNotFoundError:
        return None

    if anno not in album: #se l'anno non esiste lo aggiungo
        album[anno] = []

    album[anno].append(foto) #aggiungo la foto all'album dell'anno
    return foto

def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    for foto_lista in album.values():
        for foto in foto_lista:
            if foto['codice'] == codice:
                return f"{foto['codice']}, {foto['titolo']}, {foto['autore']}, {foto['mese']}, {foto['anno']}"
    return None


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    if anno not in album:
        return None
    titoli = [] #LISTA VUOTA IN CUI INSERIRE I TITOLI
    for foto in album[anno]:
        titoli.append(foto['titolo'])  #salvo solo i titoli dell'anno scelto
    titoli.sort() #riordino i titoli
    return titoli

def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
