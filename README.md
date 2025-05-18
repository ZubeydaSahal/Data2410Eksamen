
# DATA2410 Realiable Transport Protocol (DRTP)
Dette programmet implementerer av DRTP-DATA2410 Reliable transport Protocol. DRTP er en forenklet pålitelig transportprotokoll som er utviklet på toppen av UDP. Protokollen skal sørge for at data overføres på en sikker måte uten tap eller duplikater av pakker mellom klient og server. 

# Hvordan kjører programmed med Python 3:
DRTP-programmet kan kjøres i enten **servermodus** eller **klientmodus**, og bruker ulike kommandoflagg.



### klient modus: ###
Hvis du vile kjøre programmet i klient modus. Bruk denne kommando:

   ``` python3 application.py3 -c -f iceland-safiqul.jpg -i 127.0.0.1 -p 8080  ```

Parameter man bruker for å kjøre:
  -  -c starter i klientmodus
  -  -i serverens IP-adresse
  -  -p serveren portnummer
  -  -f navn på filen som skal sendes til serveren. i dette prosjektet er          det iceland-safiqul.jpg
  -  -w er vindusstørrelse. brukte denne til å teste ulike størrelser 

### Server modus ###
Hvis du vile kjøre programmet i server modus. Bruk denne kommando:

  ``` python3 application.py3 -s -i 10.0.1.2 -p 8080 for server. -s starter i servermodus, -p er portnummer  ```

Parameter man bruker for å kjøre:
  - -s starer i servermodus
  - -i IP-adresse serveren skal binde seg til
  - -p serveren portnummer
  - -d brukes til å ignorere en pakke for å simulere pakketap. Bruker den i       diskusjon delen for å teste pakketap


### Testing og eksperimenter ###
- Testet denne i mininet ved hjelp av simple-topo.py
- tc-netem brukte for å simulere RTT og pakketap for 2% ,5% og 50%
- -w brukte til å teste sliding window effektet
- -d brukte for å analysere Go-Back-N algoritmen ved pakketap 



    
  

