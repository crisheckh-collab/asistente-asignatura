# Resultados de las pruebas

Fecha: 25/11/2026 09:49 · Modelo: `groq:openai/gpt-oss-120b`

## 1. ¿Qué pasa si entrego tarde una práctica?

*Caso: Solo documentalista*

**Traza:**

1. **supervisor** → documentalista: Busca en la guía docente, normas de prácticas y FAQ la información sobre la entrega tardía de una práctica: cuál es la penalización o consecuencia, si hay algún límite de tiempo máximo, si afecta a la nota mínima o a requisitos de la asignatura, y cualquier excepción o condición especial que se aplique.
2. **documentalista**: **Entrega tardía de una práctica**  | Aspecto solicitado | Información encontrada en los documentos | |--------------------|-------------------------------------------| | **Penalización o consecuencia** | - Si la práctica se entrega **con hasta 48 h de retraso**, se corrige **sobre 7** en lugar de sobre **10** (es decir, la puntuación máxima se reduce).<br>- **Pasadas las 48 h**, la práctica **no se corrige** y **cuenta como un 0**. | | **Límite de tiempo máximo** | El límite máximo para recibir alguna puntuación es **48 h** después de la fecha límite oficial. Después de ese plazo la práctica se considera no entregada y recibe 0. | | **Afectación a la nota mínima o a requisitos de la asignatura** | No se menciona ninguna modificación del requisito de nota mínima (4/10 en el examen) ni de los requisitos de la asignatura. La penalización solo impacta la puntuación de la práctica (sobre 7 en lugar de 10 o 0). | | **Excepciones o condiciones especiales** | No aparecen excepciones adicionales en los documentos consultados; la regla se aplica de forma general a todas las prácticas. |  **Fuentes**    - *Normas de prácticas de Fundamentos de IA*: “Una práctica entregada con hasta 48 horas de retraso se corrige sobre 7 en lugar de sobre 10. Pasadas las 48 horas, la práctica no se corrige y cuenta como un 0.”【2†L1-L4】    No se encontró información adicional sobre excepciones, impacto en la nota mínima o requisitos de la asignatura en la guía docente ni en las preguntas frecuentes. Si la normativa cambiara, habría que consultar una actualización oficial.
3. **supervisor** → FIN

**Respuesta:**

**Entrega tardía de una práctica**

- **Hasta 48 h de retraso**: la práctica se corrige, pero la puntuación máxima pasa de **10** puntos a **7** puntos.  
- **Más de 48 h de retraso**: la práctica **no se corrige** y se registra como **0**.

Esta penalización afecta únicamente a la nota de la práctica; no modifica el requisito de nota mínima del examen (4/10) ni otros requisitos de la asignatura.

> Fuente: *Normas de prácticas de Fundamentos de IA*: “Una práctica entregada con hasta 48 horas de retraso se corrige sobre 7 en lugar de sobre 10. Pasadas las 48 horas, la práctica no se corrige y cuenta como un 0.”【2†L1-L4】

---

## 2. ¿Puedo usar asistentes de IA en las prácticas?

*Caso: Solo documentalista*

**Traza:**

1. **supervisor** → documentalista: Consultar en la guía docente, normas de prácticas y FAQ si está permitido usar asistentes de IA en las prácticas. Proveer la normativa específica, cualquier restricción, nota mínima o requisito relacionado con el uso de IA en las prácticas.
2. **documentalista**: **Uso de asistentes de IA en las prácticas**  - **Permitido**: sí, está autorizado usar herramientas de IA en la realización de las prácticas.   - **Requisito obligatorio**: en la memoria o informe de la práctica debe indicarse **qué herramienta de IA se utilizó y para qué fin**.   - **Consecuencia de no cumplir el requisito**: si no se menciona el uso de la IA, se considerará un caso de plagio y se sancionará como tal.    > “¿Puedo usar asistentes de IA en las prácticas? **Sí, siempre que se indique en la memoria qué herramienta se usó y para qué. No indicarlo se trata igual que un plagio**.” – *Preguntas frecuentes de Fundamentos de IA*【preguntas_frecuentes.md】    No aparecen otras restricciones, notas mínimas o excepciones en la guía docente ni en las normas de prácticas. Por lo tanto, la única normativa específica relativa al uso de IA en las prácticas es la citada arriba.
3. **supervisor** → FIN

**Respuesta:**

Sí, puedes usar asistentes de IA en la realización de las prácticas, **pero es obligatorio que en la memoria o informe de la práctica indiques qué herramienta de IA utilizaste y con qué fin**.  

> “¿Puedo usar asistentes de IA en las prácticas? **Sí, siempre que se indique en la memoria qué herramienta se usó y para qué. No indicarlo se trata igual que un plagio**.” – *Preguntas frecuentes de Fundamentos de IA*【preguntas_frecuentes.md】  

Si no mencionas el uso de la IA, se considerará un caso de plagio y se sancionará como tal. No existen otras restricciones, notas mínimas o excepciones en la guía docente.

---

## 3. ¿Cuál es la media ponderada de un 8 con peso 50, un 5 con peso 30 y un 9 con peso 20?

*Caso: Solo calculadora*

**Traza:**

1. **supervisor** → calculadora: Calcular la media ponderada de las notas: 8 con peso 50, 5 con peso 30 y 9 con peso 20.
2. **calculadora**: La media ponderada de esas tres notas es **7,3**.
3. **supervisor** → FIN

**Respuesta:**

La media ponderada de las notas 8 (peso 50), 5 (peso 30) y 9 (peso 20) es **7,3**【calculadora】.

---

## 4. Tengo un 6 en prácticas y un 7 en participación. ¿Qué nota necesito en el examen para aprobar?

*Caso: Documentalista + calculadora*

**Traza:**

1. **supervisor** → documentalista: Necesito los pesos de la práctica, la participación y el examen en la evaluación de la asignatura, así como la nota mínima requerida para aprobar y cualquier norma o excepción relacionada con el cálculo de la nota final.
2. **documentalista**: **Pesos de la evaluación**  | Concepto | Peso en la nota final | |----------|----------------------| | Examen final | **50 %** | | Prácticas | **30 %** | | Participación en clase | **20 %** |  *Fuente: Guía docente – “Sistema de evaluación”*【guia_docente.md】  **Nota mínima requerida para aprobar**  - La asignatura se aprueba con una **nota final de 5 sobre 10**.     *Fuente: Guía docente – “Sistema de evaluación”*【guia_docente.md】  **Normas o excepciones relacionadas con el cálculo de la nota final**  1. **Mínimo en el examen para que la media sea válida**      - Es necesario obtener al menos **4 sobre 10 en el examen final**.      - Si el estudiante no alcanza ese mínimo, **la nota final será la del examen** (no se calcula la media ponderada).      *Fuente: Guía docente – “Sistema de evaluación”*【guia_docente.md】  2. **Convocatoria extraordinaria**      - En caso de suspender la convocatoria ordinaria, el alumno puede presentarse a la extraordinaria.      - En la extraordinaria **se conservan la nota de prácticas y la de participación**, y solo se repite el examen final.      *Fuente: Guía docente – “Convocatoria extraordinaria”*【guia_docente.md】  3. **Participación**      - La participación vale el **20 %** de la nota, pero solo se puede obtener asistiendo a las sesiones.      *Fuente: Preguntas frecuentes – “¿Es obligatoria la asistencia?”*【preguntas_frecuentes.md】  4. **Prácticas**      - Las cuatro prácticas tienen el mismo peso dentro del 30 % asignado a prácticas.      - Entregas con retraso de hasta 48 h se corrigen sobre 7 en lugar de sobre 10; retrasos mayores a 48 h se califican con 0 y no se corrigen.      *Fuente: Normas de prácticas – “Entregas” y “Entregas con retraso”*【normas_practicas.md】  Estos son los datos exactos que aparecen en la documentación oficial de la asignatura. Si necesitas más detalle sobre alguna de las normas, házmelo saber.
3. **supervisor** → calculadora: Calcular la nota mínima necesaria en el examen final para alcanzar una nota final de al menos 5, dado que la nota de prácticas es 6 (peso 30%) y la nota de participación es 7 (peso 20%). Considerar también la norma de que el examen debe ser al menos 4 para que la media ponderada sea válida.
4. **calculadora**: Para alcanzar una nota final de 5, el examen debería ser 3,6; sin embargo, por la norma que exige al menos 4 en el examen, la nota mínima necesaria es **4**.
5. **supervisor** → FIN

**Respuesta:**

Para que la nota final sea **≥ 5** se combina el peso de cada componente:

* Prácticas (30 %): 6 × 0,30 = 1,8  
* Participación (20 %): 7 × 0,20 = 1,4  

Con esas dos notas ya tienes **1,8 + 1,4 = 3,2** puntos en la media ponderada.

Para alcanzar 5 puntos necesitas **5 – 3,2 = 1,8** puntos más del examen.  
Como el examen vale el 50 % de la nota, la calificación mínima requerida en el examen sería:

\[
\frac{1,8}{0,5}=3,6
\]

Sin embargo, la normativa establece que **el examen debe ser al menos 4 sobre 10** para que la media sea válida【guia_docente.md】. Si obtienes menos de 4, la nota final será la del examen y no se calcula la media ponderada.

**Conclusión:** Necesitas **al menos un 4** en el examen para aprobar la asignatura. (Con 4 obtendrías una nota final de 3,2 + 0,5 × 4 = 5,2).  

Fuentes:  
- Peso de cada componente y nota mínima de aprobación【guia_docente.md】  
- Mínimo exigido en el examen para que la media sea válida【guia_docente.md】  

---

## 5. Si saco un 8 en el examen, un 5 en prácticas y un 9 en participación, ¿qué nota final tengo?

*Caso: Documentalista + calculadora*

**Traza:**

1. **supervisor** → documentalista: Necesito los pesos de examen, prácticas y participación según la guía docente, así como cualquier norma de nota mínima o requisito adicional para la asignatura.
2. **documentalista**: **Pesos de la evaluación (según la guía docente)**    - Examen final: **50 %** de la nota final.   - Prácticas: **30 %** de la nota final.   - Participación en clase: **20 %** de la nota final.    > Fuente: *guia_docente.md* – “La nota final se calcula con tres partes: examen final (50 %), prácticas (30 %) y participación en clase (20 %).”    **Normas de nota mínima y requisitos adicionales**    1. **Nota mínima en el examen final**      - Es necesario obtener al menos **4 sobre 10** en el examen final para que se pueda calcular la media con los demás componentes.      - Si no se alcanza ese mínimo, la nota final será **la del examen**.       > Fuente: *guia_docente.md* – “Para poder hacer la media hace falta sacar al menos un 4 sobre 10 en el examen final. Si no se llega a ese mínimo, la nota final es la del examen.”    2. **Aprobación de la asignatura**      - La asignatura se aprueba con una **nota final de 5 sobre 10** o superior.       > Fuente: *guia_docente.md* – “La asignatura se aprueba con un 5 sobre 10 en la nota final.”    3. **Requisito para la participación**      - La participación solo se puede conseguir **asistiendo a las sesiones**; la asistencia no es obligatoria, pero la participación vale el 20 % de la nota.       > Fuente: *preguntas_frecuentes.md* – “La participación en clase vale un 20 % de la nota y solo se puede conseguir asistiendo a las sesiones.”    Estos son los pesos y las condiciones mínimas que aparecen en los documentos oficiales de la asignatura.
3. **supervisor** → calculadora: Calcula la nota final con examen=8, practicas=5, participacion=9 usando pesos 50%,30%,20% y verifica que el examen cumple el mínimo de 4.
4. **calculadora**: La nota final ponderada es 7.3 y, como el examen obtuvo 8 (≥ 4), cumple el requisito mínimo.
5. **supervisor** → FIN

**Respuesta:**

**Cálculo de la nota final**

- Examen (8 / 10) × 50 % = 4.0  
- Prácticas (5 / 10) × 30 % = 1.5  
- Participación (9 / 10) × 20 % = 1.8  

**Nota final = 4.0 + 1.5 + 1.8 = 7.3**

**Comprobaciones**

- El examen tiene 8 ≥ 4, por lo que se permite calcular la media (cumple la nota mínima del examen)【guia_docente.md】.  
- La nota final calculada es 7.3, superior al 5 necesario para aprobar la asignatura【guia_docente.md】.  

**Resultado:** Tu nota final sería **7.3** (aprobas la asignatura).  

*Fuentes:*  
- Pesos de la evaluación y requisito de nota mínima en el examen【guia_docente.md】.  
- Condición de participación (asistencia)【preguntas_frecuentes.md】.  
- Cálculo previo indicado en la herramienta de cálculo【calculadora】.

---

## 6. ¿Cuál es la capital de Australia?

*Caso: Fuera de la asignatura*

**Traza:**

1. **supervisor** → FIN

**Respuesta:**

No dispongo de información suficiente para responder a la pregunta.

---
