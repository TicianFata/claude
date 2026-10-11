/* generálva: make_assets.py – a túrák csomópontjai és a pontfelhő-bemutatók listája */
window.BD_TOURS = {
 "szinhaz": {
  "label": "Színház",
  "poster": "assets/img/szinhaz-nezoter.jpg",
  "scenes": [
   {
    "id": "szinpad",
    "title": "Színpad",
    "pano": "szinhaz-szinpad",
    "yaw": 0,
    "pitch": -4,
    "hotspots": [
     {
      "yaw": -0.0,
      "pitch": -8.79,
      "scene": "nezoter",
      "text": "Nézőtér"
     },
     {
      "yaw": -0.0,
      "pitch": 3.46,
      "scene": "paholy",
      "text": "Páholy"
     }
    ]
   },
   {
    "id": "nezoter",
    "title": "Nézőtér",
    "pano": "szinhaz-nezoter",
    "yaw": 0,
    "pitch": -4,
    "hotspots": [
     {
      "yaw": 0.0,
      "pitch": -3.47,
      "scene": "szinpad",
      "text": "Színpad"
     },
     {
      "yaw": 180.0,
      "pitch": 10.23,
      "scene": "paholy",
      "text": "Páholy"
     }
    ]
   },
   {
    "id": "paholy",
    "title": "Páholy",
    "pano": "szinhaz-paholy",
    "yaw": 0,
    "pitch": -4,
    "hotspots": [
     {
      "yaw": 0.0,
      "pitch": -10.48,
      "scene": "szinpad",
      "text": "Színpad"
     },
     {
      "yaw": 0.0,
      "pitch": -21.88,
      "scene": "nezoter",
      "text": "Nézőtér"
     }
    ]
   }
  ]
 },
 "szalloda": {
  "label": "Szállodai lakosztály",
  "poster": "assets/img/szalloda-lounge.jpg",
  "scenes": [
   {
    "id": "bejarat",
    "title": "Bejárat",
    "pano": "szalloda-bejarat",
    "yaw": 0,
    "pitch": -4,
    "hotspots": [
     {
      "yaw": -39.17,
      "pitch": -23.3,
      "scene": "agy",
      "text": "Ágy"
     },
     {
      "yaw": -3.05,
      "pitch": -11.29,
      "scene": "ablak",
      "text": "Ablak"
     }
    ]
   },
   {
    "id": "agy",
    "title": "Ágy",
    "pano": "szalloda-agy",
    "yaw": 0,
    "pitch": -4,
    "hotspots": [
     {
      "yaw": 140.83,
      "pitch": -23.3,
      "scene": "bejarat",
      "text": "Bejárat"
     },
     {
      "yaw": 20.56,
      "pitch": -16.31,
      "scene": "ablak",
      "text": "Ablak"
     }
    ]
   },
   {
    "id": "ablak",
    "title": "Ablak",
    "pano": "szalloda-ablak",
    "yaw": 0,
    "pitch": -4,
    "hotspots": [
     {
      "yaw": -3.05,
      "pitch": -11.29,
      "scene": "bejarat",
      "text": "Bejárat"
     },
     {
      "yaw": 20.56,
      "pitch": -16.31,
      "scene": "agy",
      "text": "Ágy"
     }
    ]
   }
  ]
 },
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
      "yaw": -0.0,
      "pitch": -3.2,
      "scene": "szinpad",
      "text": "Színpad előtt"
     },
     {
      "yaw": 93.76,
      "pitch": -2.48,
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
      "yaw": 0.0,
      "pitch": -3.2,
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
      "yaw": 3.76,
      "pitch": -2.48,
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
 },
 "muzeum": {
  "label": "Múzeum",
  "poster": "assets/img/muzeum-terem.jpg",
  "scenes": [
   {
    "id": "bejarat",
    "title": "Bejárat",
    "pano": "muzeum-bejarat",
    "yaw": 0,
    "pitch": -4,
    "hotspots": [
     {
      "yaw": 6.23,
      "pitch": -7.97,
      "scene": "kozep",
      "text": "Terem közepe"
     },
     {
      "yaw": -4.84,
      "pitch": -4.99,
      "scene": "kiallitas",
      "text": "Időszakos kiállítás"
     }
    ]
   },
   {
    "id": "kozep",
    "title": "Terem közepe",
    "pano": "muzeum-kozep",
    "yaw": 0,
    "pitch": -4,
    "hotspots": [
     {
      "yaw": -173.77,
      "pitch": -7.97,
      "scene": "bejarat",
      "text": "Bejárat"
     },
     {
      "yaw": -21.95,
      "pitch": -12.11,
      "scene": "kiallitas",
      "text": "Időszakos kiállítás"
     }
    ]
   },
   {
    "id": "kiallitas",
    "title": "Időszakos kiállítás",
    "pano": "muzeum-kiallitas",
    "yaw": 0,
    "pitch": -4,
    "hotspots": [
     {
      "yaw": 175.16,
      "pitch": -4.99,
      "scene": "bejarat",
      "text": "Bejárat"
     },
     {
      "yaw": 158.05,
      "pitch": -12.11,
      "scene": "kozep",
      "text": "Terem közepe"
     }
    ]
   }
  ]
 }
};
window.BD_CLOUD_LIST = [
 {
  "id": "szinhaz",
  "label": "Színházterem",
  "poster": "assets/img/svc-pontfelho.jpg",
  "seg": [
   "szinhaz"
  ]
 }
];
