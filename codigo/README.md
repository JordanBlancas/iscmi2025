# Proyecto de Evaluación con Lógica Difusa

Este proyecto implementa el sistema de evaluación continua basado en lógica difusa descrito en el artículo IEEE "Continuous Assessment in Remote Environments Focused on Meaningful Learning: Fuzzy Logic as an Objective Grading Tool".

## Estructura del Proyecto

```
codigo/
├── fuzzy_assessment.py    # Sistema principal de lógica difusa
├── data_generator.py      # Generador de datos de prueba
├── evaluation.py          # Evaluación y comparación
├── requirements.txt       # Dependencias
└── README.md             # Este archivo
```

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso Rápido

### 1. Ejecutar el sistema completo:
```python
# Evaluación completa con comparación
python evaluation.py
```

### 2. Usar solo el sistema difuso:
```python
from fuzzy_assessment import FuzzyAssessmentSystem

sistema = FuzzyAssessmentSystem()
resultado = sistema.evaluate_student(
    participacion=85,
    puntualidad=90, 
    calidad_trabajos=80,
    autoevaluacion=75,
    colaboracion=88
)
print(f"Calificación: {resultado['calificacion_numerica']}/20")
```

### 3. Generar datos de prueba:
```python
from data_generator import StudentDataGenerator

generator = StudentDataGenerator()
students_df = generator.generate_realistic_student_data(n_students=50)
```

## Variables del Sistema

El sistema evalúa 5 variables principales:

- **Participación** (0-100%): Nivel de participación en clases y actividades
- **Puntualidad** (0-100%): Cumplimiento de plazos de entrega
- **Calidad de Trabajos** (0-100%): Calidad técnica y conceptual de entregas
- **Autoevaluación** (0-100%): Capacidad de reflexión y autocrítica
- **Colaboración** (0-100%): Trabajo en equipo y ayuda a compañeros

## Salida

- **Calificación Final**: Escala vigesimal (0-20)
- **Categorías**: Deficiente, Regular, Buena, Excelente

## Características

✅ **Implementación completa** del sistema de lógica difusa
✅ **Reglas basadas en conocimiento experto** educativo
✅ **Generación de datos realistas** para validación
✅ **Comparación con métodos tradicionales**
✅ **Visualizaciones** de funciones de membresía y resultados
✅ **Métricas de evaluación** y reportes automáticos

## Archivos Generados

- `datos/estudiantes_datos.csv`: Datos de estudiantes generados
- `datos/resultados_evaluacion.csv`: Resultados de evaluación completa
- `figuras/comparacion_sistemas.png`: Gráficos comparativos
- `figuras/funciones_membresia.png`: Visualización del sistema difuso

## Validación

El sistema incluye:
- **Tests estadísticos** de normalidad y diferencias de medias
- **Análisis de correlación** entre métodos
- **Métricas de fairness** por perfil de estudiante
- **Comparación cuantitativa** con sistemas tradicionales

## Resultados Esperados

Basado en la investigación, el sistema debería mostrar:
- Mayor consistencia en calificaciones
- Mejor captura de competencias transversales
- Evaluación más justa para diferentes perfiles de estudiantes
- Reducción de sesgos en evaluación remota