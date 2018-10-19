;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-reader.ss" "lang")((modname Pract_3) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))

(require 2htdp/batch-io)

;; Principios

;; Definir una función por cada tarea

;; Por cada constante mencionada en la declaración de un problema introducir una
;; definición constante

(define NR "\n")

(define (carta nombre apellido  firma-nombre)
  (string-append
   (saludo nombre)
   NR
   (cuerpo  nombre apellido)
   NR
   (despedida firma-nombre)))

(define (saludo nombre)
  (string-append "Estimado " nombre ","))

(define (cuerpo  nombre apellido)
  (string-append
   "Hemos descubierto que todas las personas con el apellido "
   NR
   apellido  " han ganado la lotería. Por lo tanto, " nombre ", "
   NR
   "apúrate a recoger tu premio."))

(define (despedida firma-nombre)
  (string-append
   "Atentamente,"
   NR
   firma-nombre))
; (carta "Emma" "Fuentes" "Odin Arrow")
(write-file 'stdout (carta "Emma" "Fuentes" "Odin Arrow"))
