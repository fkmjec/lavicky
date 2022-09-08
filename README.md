# Minuty nabíjení ze zásuvek u veřejných laviček a venkovní teplota
V roce 2017 se do ulic Prahy v rámci pilotního projektu dostalo několik chytrých laviček.
Tyto lavičky jednak umožňují např. zjišťovat aktuální teplotu nebo přivolat pomoc, ale také
na sobě mají USB porty, ze kterých si občané města mohou nabít telefon.

Operátor ICT, který lavičky provozuje, mezi 5.9.2017 a 31.1.2018 sbíral data o využívání USB portů,
konkrétně za každý den celkový počet minut nabíjení. Mým cílem je v rámci práce zjistit, zda
počet minut nabíjení souvisí s teplotou daný den v Praze.

Data jsem o nabíjení čerpal jednak z již zmíněného [datasetu Operátora ICT](https://opendata.praha.eu/dataset/lavicky-api-usb), konkrétně z CSV, které obsahuje celkový počet minut u laviček z Alšova nábřeží. Jako data o teplotě jsem použil [dataset z pražského Klementina](https://www.chmi.cz/historicka-data/pocasi/praha-klementinum). Data o teplotě byla ve formátu `.xlsx`, jeho převod na CSV jsem provedl pomocí nástroje `ssconvert`.
