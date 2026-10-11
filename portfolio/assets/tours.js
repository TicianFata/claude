/* generálva: make_assets.py – a túrák csomópontjai és a pontfelhő-bemutatók listája */
window.BD_TOURS = {
 "rendezveny": {
  "label": "Rendezvényhelyszín",
  "poster": "assets/img/rendezveny-hero.jpg",
  "scenes": [
   {
    "id": "asztalok",
    "title": "Vendégtér",
    "pano": "rendezveny-asztalok",
    "yaw": 0,
    "pitch": -4,
    "hotspots": [
     {
      "yaw": -5.96,
      "pitch": -2.8,
      "scene": "szinpad",
      "text": "Színpad előtt"
     },
     {
      "yaw": 87.51,
      "pitch": -2.74,
      "scene": "bejarat",
      "text": "Kastély előtt"
     }
    ]
   },
   {
    "id": "szinpad",
    "title": "Színpad előtt",
    "pano": "rendezveny-szinpad",
    "yaw": 0,
    "pitch": -4,
    "hotspots": [
     {
      "yaw": -5.96,
      "pitch": -2.8,
      "scene": "asztalok",
      "text": "Vendégtér"
     },
     {
      "yaw": -49.9,
      "pitch": -1.9,
      "scene": "bejarat",
      "text": "Kastély előtt"
     }
    ]
   },
   {
    "id": "bejarat",
    "title": "Kastély előtt",
    "pano": "rendezveny-bejarat",
    "yaw": 0,
    "pitch": -4,
    "hotspots": [
     {
      "yaw": -2.49,
      "pitch": -2.74,
      "scene": "asztalok",
      "text": "Vendégtér"
     },
     {
      "yaw": 40.1,
      "pitch": -1.9,
      "scene": "szinpad",
      "text": "Színpad előtt"
     }
    ]
   }
  ]
 }
};
window.BD_CLOUD_LIST = [
 {
  "id": "muzeum",
  "label": "Múzeum – kiállítóterem",
  "poster": "assets/img/muzeum-pontfelho-felul.jpg",
  "seg": [
   "muzeum"
  ]
 },
 {
  "id": "rendezveny",
  "label": "Rendezvényhelyszín – tervezett elrendezéssel",
  "poster": "assets/img/rendezveny-pontfelho-terv.jpg",
  "seg": [
   "rendezveny"
  ]
 },
 {
  "id": "szinhaz",
  "label": "Színházterem",
  "poster": "assets/img/svc-pontfelho.jpg",
  "seg": [
   "szinhaz"
  ]
 }
];
