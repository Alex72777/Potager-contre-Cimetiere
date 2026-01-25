# Potager contre cimetiere

Projet piles et files Terminale

`python3 main.py`

tree -I \_\_pycache\_\_ | sed 's/$/ /'

.  
├── README.md  
└── src  
├── entities  
│ ├── lawnmoyersClass.py  
│ ├── plantsClass.py  
│ └── zombiesClass.py  
├── events  
│ ├── eventClass.py  
│ ├── event_display_text.py  
│ ├── event_invoke_zombie.py  
│ └── event_seizure.py  
├── gameClass.py  
├── livingentities  
│ ├── livinglawnmoyers  
│ │ └── livinglawnmoyerClass.py  
│ ├── livingplants  
│ │ ├── livinglandmine.py  
│ │ ├── livingPeashooter.py  
│ │ ├── livingplantClass.py  
│ │ ├── livingSunflower.py  
│ │ └── livingWallnut.py  
│ └── livingzombies  
│ └── livingzombieClass.py  
├── main.py  
├── playerClass.py  
└── ui  
├── houseslot.py  
├── lane.py  
├── plantselector.py  
└── slot.py  

9 directories, 22 files  

find -type f -name "\*.py" -exec wc -l {} + | sort -rn -k1 | sed 's/$/ /'  

1184 total  
166 ./src/ui/lane.py  
145 ./src/gameClass.py  
125 ./src/ui/slot.py  
78 ./src/livingentities/livingzombies/livingzombieClass.py  
70 ./src/entities/plantsClass.py  
68 ./src/livingentities/livingplants/livinglandmine.py  
59 ./src/livingentities/livinglawnmoyers/livinglawnmoyerClass.py  
54 ./src/playerClass.py  
51 ./src/livingentities/livingplants/livingplantClass.py  
51 ./src/events/event_display_text.py  
50 ./src/livingentities/livingplants/livingPeashooter.py  
46 ./src/ui/plantselector.py  
43 ./src/livingentities/livingplants/livingSunflower.py  
40 ./src/events/eventClass.py  
33 ./src/events/event_invoke_zombie.py  
27 ./src/livingentities/livingplants/livingWallnut.py  
27 ./src/events/event_seizure.py  
23 ./src/ui/houseslot.py  
16 ./src/entities/zombiesClass.py  
7 ./src/main.py  
5 ./src/entities/lawnmoyersClass.py  
