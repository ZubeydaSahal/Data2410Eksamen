
# DATA2410 Realiable Transport Protocol (DRTP)
================================================================
Dette programmet implementerer av DRTP-DATA2410 Reliable transport Protocol. DRTP er en forenklet pålitelig transportprotokoll som er utviklet på toppen av UDP. Protokollen skal sørge for at data overføres på en sikker måte uten tap eller duplikater av pakker mellom klient og server. 

# Hvordan kjører programmed med Python 3:
DRTP programmet kan bli kjørt i enten server eller klient mode. Disse har ulike flagg som brukes.


# klient modus:
Hvis du vile kjøre programmet i klient modus. Bruker man denne:

python3 application.py3 -c -f iceland-safiqul.jpg -i 127.0.0.1 -p 8080

Parameter man bruker for å kjøre:
  -  -c starter i klientmodus
  -  -i Serveren IP-adresse
  -  -p Serveren portnummer
  -  -f navn på filen som skal sendes til serveren. i denne oppgaven heter         filen iceland-safiqul.jpg
  -  -w er vindusstørrelse. brukte denne til å teste ulike størrelser 

# Server modus
Hvis du vile kjøre programmet i server modus. Bruker man denne:
python3 application.py3 -s -i 10.0.1.2 -p 8080 for server. -s starter i servermodus, -p er portnummer 

Parameter man bruker for å kjøre:
  - -s Starer i servermodus
  - -i Serveren IP-adresse
  - -p Serveren portnummer
  - -d brukes til å ignorere pakker. bruker denne i discusion delen for å teste pakketap
    
  

