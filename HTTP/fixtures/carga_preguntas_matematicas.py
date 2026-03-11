#!/usr/bin/env python3
"""
Script para crear 100 preguntas de matemáticas para el banco de preguntas (sin prueba asignada).

Uso:
    Desde la raíz del proyecto Django:
        python manage.py shell < HTTP/fixtures/carga_preguntas_matematicas.py
"""
import random
from django.db import transaction
from prueba_diagnostica.models import PreguntaDiagnostica, RespuestaDiagnostica

def main():
    print("Iniciando carga de preguntas de matemáticas al BANCO DE PREGUNTAS...")
    
    created_count = 0
    
    with transaction.atomic():
        for i in range(100):
            # Generar operación matemática aleatoria
            operacion = random.choice(['suma', 'resta', 'multiplicacion'])
            
            if operacion == 'suma':
                a = random.randint(1, 100)
                b = random.randint(1, 100)
                resultado = a + b
                texto_pregunta = f"¿Cuánto es {a} + {b}?"
                explicacion = f"{a} más {b} es igual a {resultado}"
            elif operacion == 'resta':
                a = random.randint(1, 100)
                b = random.randint(1, 100)
                # Asegurar resultado positivo para simplificar
                if a < b: a, b = b, a
                resultado = a - b
                texto_pregunta = f"¿Cuánto es {a} - {b}?"
                explicacion = f"{a} menos {b} es igual a {resultado}"
            else: # multiplicacion
                a = random.randint(1, 12)
                b = random.randint(1, 12)
                resultado = a * b
                texto_pregunta = f"¿Cuánto es {a} x {b}?"
                explicacion = f"{a} por {b} es igual a {resultado}"

            # Crear la pregunta con id_prueba=None (Banco de preguntas)
            pregunta = PreguntaDiagnostica.objects.create(
                id_prueba=None,
                texto_pregunta=texto_pregunta,
                tipo_pregunta='multiple',
                puntaje=1.0,
                explicacion=explicacion,
                estado=True
            )

            # Generar respuestas (1 correcta y 3 incorrectas)
            respuestas_data = []
            
            # Respuesta correcta
            respuestas_data.append({
                "texto_respuesta": str(resultado),
                "es_correcta": True
            })
            
            # Respuestas incorrectas
            generated_answers = {resultado}
            while len(respuestas_data) < 4:
                # Generar respuesta incorrecta cercana
                offset = random.randint(-10, 10)
                if offset == 0: continue
                
                fake_ans = resultado + offset
                if fake_ans < 0 and operacion != 'resta': continue # Evitar negativos si no es resta
                
                if fake_ans not in generated_answers:
                    generated_answers.add(fake_ans)
                    respuestas_data.append({
                        "texto_respuesta": str(fake_ans),
                        "es_correcta": False
                    })
            
            # Mezclar respuestas
            random.shuffle(respuestas_data)
            
            # Crear respuestas en BD
            for resp in respuestas_data:
                RespuestaDiagnostica.objects.create(
                    id_pregunta=pregunta,
                    texto_respuesta=resp["texto_respuesta"],
                    es_correcta=resp["es_correcta"]
                )
            
            created_count += 1
            if created_count % 10 == 0:
                print(f"Creadas {created_count} preguntas básicas...")

        print("Iniciando carga de preguntas con LaTeX...")
        for i in range(100):
            tipo = random.choice(['ecuacion', 'fraccion', 'potencia', 'raiz'])
            
            if tipo == 'ecuacion':
                # ax + b = c
                x = random.randint(1, 12)
                a = random.randint(2, 6)
                b = random.randint(1, 20)
                c = a * x + b
                
                texto_pregunta = f"Resuelve la siguiente ecuación para encontrar el valor de $x$: $${a}x + {b} = {c}$$"
                resultado_correct = str(x)
                explicacion = f"Para despejar $x$, restamos {b} a ambos lados: ${a}x = {c-b}$. Luego dividimos por {a}: $x = {x}$."
                
                # Distractores
                distractores = set()
                while len(distractores) < 3:
                    fake = x + random.randint(-5, 5)
                    if fake != x and fake > 0: # Asumimos x positivo para simplificar
                        distractores.add(str(fake))

            elif tipo == 'fraccion':
                # Suma de fracciones homogéneas: a/d + b/d
                den = random.randint(2, 9)
                num1 = random.randint(1, 10)
                num2 = random.randint(1, 10)
                
                texto_pregunta = f"Calcula la suma de las siguientes fracciones: $$\\frac{{{num1}}}{{{den}}} + \\frac{{{num2}}}{{{den}}}$$"
                
                res_num = num1 + num2
                resultado_correct = f"$\\frac{{{res_num}}}{{{den}}}$"
                explicacion = f"Como los denominadores son iguales, sumamos los numeradores: ${num1} + {num2} = {res_num}$. El resultado es $\\frac{{{res_num}}}{{{den}}}$."
                
                # Distractores
                distractores = set()
                while len(distractores) < 3:
                    fake_num = res_num + random.randint(-3, 3)
                    if fake_num != res_num and fake_num > 0:
                        distractores.add(f"$\\frac{{{fake_num}}}{{{den}}}$")

            elif tipo == 'potencia':
                base = random.randint(2, 6)
                exp = random.randint(2, 3)
                val = base ** exp
                
                texto_pregunta = f"Calcula el valor de la siguiente potencia: $${base}^{{{exp}}}$$"
                resultado_correct = str(val)
                explicacion = f"Multiplicamos {base} por sí mismo {exp} veces: {base} " + " x ".join([str(base)]*(exp-1)) + f" = {val}."
                
                # Distractores
                distractores = set()
                while len(distractores) < 3:
                    fake = val + random.randint(-10, 10)
                    if fake != val and fake > 0:
                        distractores.add(str(fake))

            elif tipo == 'raiz':
                raiz = random.randint(2, 15)
                radicando = raiz * raiz
                
                texto_pregunta = f"Calcula la raíz cuadrada: $$\\sqrt{{{radicando}}}$$"
                resultado_correct = str(raiz)
                explicacion = f"Buscamos un número que multiplicado por sí mismo dé {radicando}. Ese número es {raiz}."
                
                # Distractores
                distractores = set()
                while len(distractores) < 3:
                    fake = raiz + random.randint(-5, 5)
                    if fake != raiz and fake > 0:
                        distractores.add(str(fake))

            # Crear la pregunta
            pregunta = PreguntaDiagnostica.objects.create(
                id_prueba=None,
                texto_pregunta=texto_pregunta,
                tipo_pregunta='multiple',
                puntaje=1.0,
                explicacion=explicacion,
                estado=True
            )

            # Crear respuestas
            respuestas_objs = []
            
            # Correcta
            respuestas_objs.append(RespuestaDiagnostica(
                id_pregunta=pregunta,
                texto_respuesta=resultado_correct,
                es_correcta=True
            ))
            
            # Incorrectas
            for dist in distractores:
                respuestas_objs.append(RespuestaDiagnostica(
                    id_pregunta=pregunta,
                    texto_respuesta=dist,
                    es_correcta=False
                ))
            
            # Mezclar y guardar
            random.shuffle(respuestas_objs)
            RespuestaDiagnostica.objects.bulk_create(respuestas_objs)

            created_count += 1
            if created_count % 10 == 0:
                print(f"Creadas {created_count} preguntas totales...")

    print(f"Finalizado. Se crearon {created_count} preguntas de matemáticas en el banco de preguntas.")

if __name__ == "__main__":
    main()
