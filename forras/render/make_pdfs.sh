#!/bin/bash
# Generates the client PDFs from prezentacio.html (full + one per target group)
cd "$(dirname "$0")"
OUT=/home/user/claude/pdf
mkdir -p "$OUT"
export NODE_PATH=/opt/node22/lib/node_modules
node shoot.js deck "" pdf_full "$OUT/BrickData_Portfolio_teljes.pdf" nothumbs
node shoot.js deck "?csoport=szinhaz" pdf_sz "$OUT/BrickData_Portfolio_Szinhazak.pdf" nothumbs
node shoot.js deck "?csoport=rendezveny" pdf_r "$OUT/BrickData_Portfolio_Rendezvenyhelyszinek.pdf" nothumbs
node shoot.js deck "?csoport=szalloda" pdf_h "$OUT/BrickData_Portfolio_Szallodak.pdf" nothumbs
node shoot.js deck "?csoport=muzeum" pdf_m "$OUT/BrickData_Portfolio_Muzeumok.pdf" nothumbs
ls -la "$OUT"
