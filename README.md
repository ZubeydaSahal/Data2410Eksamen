
# DATA2410 Realiable Transport Protocol (DRTP)
Denne programmet implementerer DRTP for pålitelig filoverføring over UDP, med støtte for Go-Back-N algoritme, etablerer forbindelse og avslutter forbindelse riktig måte. Programmet kjøres med application.py, og kan startes enten som server eller klient. Programmet kjøres med application.py, og kan startes enten som server eller klient.

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
    
  

