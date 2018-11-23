#!/bin/env ruby
# encoding: utf-8

def llenaMemoria(cadena)
	return cadena.ljust(30,'-')
end

def asignaProceso(cadena)
	tamaño=0
	indice=0
	cad_aux = " "
	cad_insertar = " "
	while tamaño > 15 or tamaño < 1
		puts "Ingresa el tamaño del proceso #{$procesos}: (1-15)"
		tamaño = gets.chomp.to_i
		tamaño.to_i
		if tamaño > 15 or tamaño < 1
			puts "Ingrese un número válido\n"
		end			
	end
	
	cad_aux = cad_aux.rjust(tamaño,'-')
	cad_insertar = cad_insertar.rjust(tamaño,$procesos)
	
	if cadena.include(cad_aux)
		indice = cadena.index(cad_aux)
		cadena.slice!(indice,indice+tamaño)
		$procesos.succ
		return cadena = cadena.insert(indice,cad_insetar)
	elsif  !(cadena.include(cad_aux))
		cadena = compacta(cadena)
		if cadena.include(cad_aux)
			indice = cadena.index(cad_aux)
			cadena.slice!(indice,indice+tamaño)
			$procesos.succ
			return cadena = cadena.insert(indice,cad_insetar)
		end
	else
		liberaProceso(cadena)
		if cadena.include(cad_aux)
			indice = cadena.index(cad_aux)
			cadena.slice!(indice,indice+tamaño)
			$procesos.succ
			return cadena = cadena.insert(indice,cad_insetar)
		end
	end	
	
end

def compacta(cadena)
	cadena.delete('-')
	return llenaMemoria(cadena)
end

def liberaProceso(cadena)
	puts "Ingrese el símbolo del proceso a eliminar (p.e. A)"
	ch = gets.chomp	
	cadena.delete(ch)
	return llenaMemoria(cadena)
end

def menu()
	s = true
	cadena = ""
	cadena = llenaMemoria(cadena)	
	opcion = ""
	while s do
		puts "Agregar proceso(0)\tLiberar(1)\tSalir(5)"
		opcion = gets.chomp
		if opcion == '0'
			cadena = asignaProceso(cadena)
		elsif opcion == '1'
			cadena = liberaProceso(cadena)
		elsif opcion == '5'
			s = false
		else
			puts "Opción inválida"
		end
	puts "-------- ESTADO DE LA MEMORIA --------\n"
	puts cadena
	puts "\n"
	end
end


$procesos = "A"
menu()

