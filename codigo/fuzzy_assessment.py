"""
Sistema de Evaluación Continua con Lógica Difusa
================================================

Este módulo implementa un sistema de evaluación continua basado en lógica difusa
para entornos de aprendizaje remoto e híbrido, tal como se describe en el artículo
"Continuous Assessment in Remote Environments Focused on Meaningful Learning: 
Fuzzy Logic as an Objective Grading Tool"

Autor: Jordan Blancas
Universidad Continental, Huancayo, Perú
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class FuzzyAssessmentSystem:
    """
    Sistema de evaluación continua basado en lógica difusa.
    
    Integra múltiples variables de evaluación:
    - Participación en clases
    - Puntualidad en entregas
    - Calidad de trabajos
    - Autoevaluación
    - Colaboración
    """
    
    def __init__(self):
        """Inicializa el sistema de lógica difusa."""
        self.setup_fuzzy_variables()
        self.setup_fuzzy_rules()
        self.setup_control_system()
    
    def setup_fuzzy_variables(self):
        """Define las variables difusas de entrada y salida."""
        # Variables de entrada
        self.participacion = ctrl.Antecedent(np.arange(0, 101, 1), 'participacion')
        self.puntualidad = ctrl.Antecedent(np.arange(0, 101, 1), 'puntualidad')
        self.calidad_trabajos = ctrl.Antecedent(np.arange(0, 101, 1), 'calidad_trabajos')
        self.autoevaluacion = ctrl.Antecedent(np.arange(0, 101, 1), 'autoevaluacion')
        self.colaboracion = ctrl.Antecedent(np.arange(0, 101, 1), 'colaboracion')
        
        # Variable de salida
        self.calificacion_final = ctrl.Consequent(np.arange(0, 21, 1), 'calificacion_final')
        
        # Funciones de membresía para variables de entrada
        self._setup_input_membership_functions()
        
        # Funciones de membresía para variable de salida
        self.calificacion_final['deficiente'] = fuzz.trimf(self.calificacion_final.universe, [0, 0, 10])
        self.calificacion_final['regular'] = fuzz.trimf(self.calificacion_final.universe, [5, 10, 15])
        self.calificacion_final['buena'] = fuzz.trimf(self.calificacion_final.universe, [10, 15, 20])
        self.calificacion_final['excelente'] = fuzz.trimf(self.calificacion_final.universe, [15, 20, 20])
    
    def _setup_input_membership_functions(self):
        """Define las funciones de membresía para variables de entrada."""
        variables = [self.participacion, self.puntualidad, self.calidad_trabajos, 
                    self.autoevaluacion, self.colaboracion]
        
        for var in variables:
            var['baja'] = fuzz.trimf(var.universe, [0, 0, 50])
            var['media'] = fuzz.trimf(var.universe, [25, 50, 75])
            var['alta'] = fuzz.trimf(var.universe, [50, 100, 100])
    
    def setup_fuzzy_rules(self):
        """Define las reglas difusas basadas en el conocimiento experto."""
        self.rules = []
        
        # Reglas para calificación excelente
        self.rules.append(ctrl.Rule(
            self.participacion['alta'] & self.puntualidad['alta'] & 
            self.calidad_trabajos['alta'] & self.autoevaluacion['alta'] & 
            self.colaboracion['alta'], 
            self.calificacion_final['excelente']
        ))
        
        # Reglas para calificación buena
        self.rules.append(ctrl.Rule(
            self.participacion['alta'] & self.puntualidad['alta'] & 
            self.calidad_trabajos['alta'], 
            self.calificacion_final['buena']
        ))
        
        self.rules.append(ctrl.Rule(
            self.participacion['media'] & self.puntualidad['alta'] & 
            self.calidad_trabajos['alta'] & self.colaboracion['alta'], 
            self.calificacion_final['buena']
        ))
        
        # Reglas para calificación regular
        self.rules.append(ctrl.Rule(
            self.participacion['media'] & self.puntualidad['media'] & 
            self.calidad_trabajos['media'], 
            self.calificacion_final['regular']
        ))
        
        self.rules.append(ctrl.Rule(
            self.participacion['alta'] & self.puntualidad['baja'] & 
            self.calidad_trabajos['media'], 
            self.calificacion_final['regular']
        ))
        
        # Reglas para calificación deficiente
        self.rules.append(ctrl.Rule(
            self.participacion['baja'] & self.puntualidad['baja'], 
            self.calificacion_final['deficiente']
        ))
        
        self.rules.append(ctrl.Rule(
            self.calidad_trabajos['baja'] & self.autoevaluacion['baja'], 
            self.calificacion_final['deficiente']
        ))
        
        # Reglas adicionales para casos especiales
        self.rules.append(ctrl.Rule(
            self.participacion['baja'] & self.calidad_trabajos['alta'] & 
            self.puntualidad['alta'], 
            self.calificacion_final['regular']
        ))
    
    def setup_control_system(self):
        """Configura el sistema de control difuso."""
        self.control_system = ctrl.ControlSystem(self.rules)
        self.simulation = ctrl.ControlSystemSimulation(self.control_system)
    
    def evaluate_student(self, participacion: float, puntualidad: float, 
                        calidad_trabajos: float, autoevaluacion: float, 
                        colaboracion: float) -> Dict:
        """
        Evalúa a un estudiante individual usando el sistema difuso.
        
        Args:
            participacion: Nivel de participación (0-100)
            puntualidad: Puntualidad en entregas (0-100)
            calidad_trabajos: Calidad de trabajos entregados (0-100)
            autoevaluacion: Capacidad de autoevaluación (0-100)
            colaboracion: Nivel de colaboración (0-100)
        
        Returns:
            Dict con la calificación y detalles del proceso
        """
        # Asignar valores de entrada
        self.simulation.input['participacion'] = participacion
        self.simulation.input['puntualidad'] = puntualidad
        self.simulation.input['calidad_trabajos'] = calidad_trabajos
        self.simulation.input['autoevaluacion'] = autoevaluacion
        self.simulation.input['colaboracion'] = colaboracion
        
        # Ejecutar la inferencia difusa
        self.simulation.compute()
        
        # Obtener resultado
        calificacion = self.simulation.output['calificacion_final']
        
        return {
            'calificacion_numerica': round(calificacion, 2),
            'calificacion_vigesimal': round(calificacion, 2),
            'inputs': {
                'participacion': participacion,
                'puntualidad': puntualidad,
                'calidad_trabajos': calidad_trabajos,
                'autoevaluacion': autoevaluacion,
                'colaboracion': colaboracion
            }
        }
    
    def evaluate_class(self, students_data: pd.DataFrame) -> pd.DataFrame:
        """
        Evalúa a toda una clase de estudiantes.
        
        Args:
            students_data: DataFrame con datos de estudiantes
        
        Returns:
            DataFrame con calificaciones procesadas
        """
        results = []
        
        for idx, student in students_data.iterrows():
            evaluation = self.evaluate_student(
                student['participacion'],
                student['puntualidad'], 
                student['calidad_trabajos'],
                student['autoevaluacion'],
                student['colaboracion']
            )
            
            result = {
                'estudiante_id': student.get('estudiante_id', idx),
                'nombre': student.get('nombre', f'Estudiante_{idx}'),
                **evaluation['inputs'],
                'calificacion_fuzzy': evaluation['calificacion_numerica']
            }
            results.append(result)
        
        return pd.DataFrame(results)
    
    def visualize_membership_functions(self, save_path: str = None):
        """Visualiza las funciones de membresía del sistema."""
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('Funciones de Membresía del Sistema de Evaluación Difusa', 
                     fontsize=16, fontweight='bold')
        
        # Variables de entrada
        input_vars = [
            (self.participacion, 'Participación'),
            (self.puntualidad, 'Puntualidad'),
            (self.calidad_trabajos, 'Calidad de Trabajos'),
            (self.autoevaluacion, 'Autoevaluación'),
            (self.colaboracion, 'Colaboración')
        ]
        
        for i, (var, title) in enumerate(input_vars):
            ax = axes[i//3, i%3]
            var.view(ax=ax)
            ax.set_title(title)
            ax.grid(True, alpha=0.3)
        
        # Variable de salida
        ax = axes[1, 2]
        self.calificacion_final.view(ax=ax)
        ax.set_title('Calificación Final')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Gráfico guardado en: {save_path}")
        
        plt.show()
    
    def generate_sample_evaluation(self, student_name: str = "Estudiante Ejemplo") -> Dict:
        """Genera una evaluación de ejemplo para demostrar el sistema."""
        # Datos de ejemplo
        sample_data = {
            'participacion': 85,
            'puntualidad': 90,
            'calidad_trabajos': 80,
            'autoevaluacion': 75,
            'colaboracion': 88
        }
        
        result = self.evaluate_student(**sample_data)
        
        print(f"\n=== Evaluación de {student_name} ===")
        print(f"Participación: {sample_data['participacion']}%")
        print(f"Puntualidad: {sample_data['puntualidad']}%")
        print(f"Calidad de Trabajos: {sample_data['calidad_trabajos']}%")
        print(f"Autoevaluación: {sample_data['autoevaluacion']}%")
        print(f"Colaboración: {sample_data['colaboracion']}%")
        print(f"\n→ Calificación Final: {result['calificacion_numerica']}/20")
        
        return result

if __name__ == "__main__":
    # Ejemplo de uso
    print("Inicializando Sistema de Evaluación con Lógica Difusa...")
    sistema = FuzzyAssessmentSystem()
    
    # Generar evaluación de ejemplo
    resultado = sistema.generate_sample_evaluation()
    
    # Visualizar funciones de membresía
    sistema.visualize_membership_functions()