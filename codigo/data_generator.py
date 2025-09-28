"""
Generador de Datos de Prueba
============================

Este módulo genera datos sintéticos de estudiantes para validar
el sistema de evaluación con lógica difusa.
"""

import numpy as np
import pandas as pd
from typing import List, Dict
import random

class StudentDataGenerator:
    """Generador de datos realistas de estudiantes para testing."""
    
    def __init__(self, seed: int = 42):
        """Inicializa el generador con semilla aleatoria."""
        np.random.seed(seed)
        random.seed(seed)
        
        # Nombres de ejemplo
        self.nombres = [
            "Ana García", "Carlos López", "María Rodriguez", "José Martinez",
            "Lucia Fernández", "Diego Ruiz", "Carmen Morales", "Antonio Silva",
            "Patricia Jiménez", "Manuel Castro", "Isabel Torres", "Francisco Ramos",
            "Laura Herrera", "Roberto Molina", "Cristina Delgado", "Miguel Ortega",
            "Elena Vargas", "Daniel Guerrero", "Raquel Peña", "Javier Mendoza",
            "Mónica Aguilar", "Andrés Castillo", "Beatriz Romero", "Fernando Gil",
            "Natalia Vega", "Sergio Moreno", "Pilar Rubio", "Alberto Navarro"
        ]
    
    def generate_realistic_student_data(self, n_students: int = 50) -> pd.DataFrame:
        """
        Genera datos realistas de estudiantes con correlaciones lógicas.
        
        Args:
            n_students: Número de estudiantes a generar
            
        Returns:
            DataFrame con datos de estudiantes
        """
        students = []
        
        for i in range(n_students):
            # Seleccionar perfil de estudiante
            perfil = self._select_student_profile()
            
            # Generar datos basados en el perfil
            student_data = self._generate_student_by_profile(i, perfil)
            students.append(student_data)
        
        return pd.DataFrame(students)
    
    def _select_student_profile(self) -> str:
        """Selecciona un perfil de estudiante basado en distribución realista."""
        perfiles = {
            'excelente': 0.15,    # 15% estudiantes excelentes
            'bueno': 0.35,        # 35% estudiantes buenos
            'promedio': 0.35,     # 35% estudiantes promedio
            'con_dificultades': 0.15  # 15% con dificultades
        }
        
        rand = random.random()
        cumulative = 0
        
        for perfil, prob in perfiles.items():
            cumulative += prob
            if rand <= cumulative:
                return perfil
        
        return 'promedio'
    
    def _generate_student_by_profile(self, student_id: int, perfil: str) -> Dict:
        """Genera datos de estudiante según su perfil."""
        base_data = {
            'estudiante_id': student_id + 1,
            'nombre': random.choice(self.nombres)
        }
        
        if perfil == 'excelente':
            # Estudiantes excelentes: altos en todo con poca variación
            base_data.update({
                'participacion': np.random.normal(90, 5),
                'puntualidad': np.random.normal(95, 3),
                'calidad_trabajos': np.random.normal(88, 4),
                'autoevaluacion': np.random.normal(85, 6),
                'colaboracion': np.random.normal(92, 4)
            })
            
        elif perfil == 'bueno':
            # Estudiantes buenos: generalmente altos con más variación
            base_data.update({
                'participacion': np.random.normal(75, 8),
                'puntualidad': np.random.normal(80, 10),
                'calidad_trabajos': np.random.normal(78, 7),
                'autoevaluacion': np.random.normal(70, 10),
                'colaboracion': np.random.normal(76, 9)
            })
            
        elif perfil == 'promedio':
            # Estudiantes promedio: centrados con variación moderada
            base_data.update({
                'participacion': np.random.normal(60, 12),
                'puntualidad': np.random.normal(65, 15),
                'calidad_trabajos': np.random.normal(62, 10),
                'autoevaluacion': np.random.normal(58, 12),
                'colaboracion': np.random.normal(61, 11)
            })
            
        else:  # con_dificultades
            # Estudiantes con dificultades: bajos con alta variación
            base_data.update({
                'participacion': np.random.normal(40, 15),
                'puntualidad': np.random.normal(45, 18),
                'calidad_trabajos': np.random.normal(42, 12),
                'autoevaluacion': np.random.normal(38, 15),
                'colaboracion': np.random.normal(41, 14)
            })
        
        # Aplicar correlaciones lógicas y restricciones
        base_data = self._apply_logical_correlations(base_data)
        base_data = self._apply_constraints(base_data)
        base_data['perfil'] = perfil
        
        return base_data
    
    def _apply_logical_correlations(self, data: Dict) -> Dict:
        """Aplica correlaciones lógicas entre variables."""
        # La puntualidad alta tiende a correlacionar con buena participación
        if data['puntualidad'] > 80 and data['participacion'] < 60:
            data['participacion'] += random.uniform(5, 15)
        
        # Calidad de trabajos alta sugiere buena autoevaluación
        if data['calidad_trabajos'] > 75 and data['autoevaluacion'] < 50:
            data['autoevaluacion'] += random.uniform(8, 20)
        
        # Colaboración alta correlaciona con participación
        if data['colaboracion'] > 80 and data['participacion'] < 70:
            data['participacion'] += random.uniform(5, 12)
        
        return data
    
    def _apply_constraints(self, data: Dict) -> Dict:
        """Aplica restricciones para mantener valores en rango válido."""
        variables = ['participacion', 'puntualidad', 'calidad_trabajos', 
                    'autoevaluacion', 'colaboracion']
        
        for var in variables:
            data[var] = max(0, min(100, data[var]))  # Clamp entre 0-100
            data[var] = round(data[var], 1)  # Redondear a 1 decimal
        
        return data
    
    def generate_traditional_grades(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Genera calificaciones tradicionales para comparación.
        
        Simula un sistema tradicional basado principalmente en exámenes.
        """
        df_copy = df.copy()
        
        # Calificación tradicional: 70% exámenes, 20% tareas, 10% participación
        # Simulamos exámenes con más variabilidad
        examenes = np.random.normal(
            df_copy['calidad_trabajos'] * 0.8,  # Correlacionado con calidad
            15  # Alta variabilidad
        )
        
        tareas = df_copy['calidad_trabajos'] * 0.9
        participacion_peso = df_copy['participacion'] * 0.1
        
        calificacion_tradicional = (
            examenes * 0.7 + 
            tareas * 0.2 + 
            participacion_peso * 0.1
        ) / 5  # Normalizar a escala 0-20
        
        # Aplicar restricciones
        calificacion_tradicional = np.clip(calificacion_tradicional, 0, 20)
        df_copy['calificacion_tradicional'] = np.round(calificacion_tradicional, 2)
        
        return df_copy
    
    def save_to_csv(self, df: pd.DataFrame, filename: str):
        """Guarda el DataFrame en un archivo CSV."""
        filepath = f"/workspaces/iscmi2025/datos/{filename}"
        df.to_csv(filepath, index=False)
        print(f"Datos guardados en: {filepath}")
        return filepath

def main():
    """Función principal para generar datos de prueba."""
    print("Generando datos de estudiantes...")
    
    # Crear generador
    generator = StudentDataGenerator()
    
    # Generar datos de estudiantes
    students_df = generator.generate_realistic_student_data(n_students=60)
    
    # Agregar calificaciones tradicionales para comparación
    students_df = generator.generate_traditional_grades(students_df)
    
    # Mostrar estadísticas
    print(f"\nDatos generados para {len(students_df)} estudiantes")
    print("\nDistribución por perfil:")
    print(students_df['perfil'].value_counts())
    
    print("\nEstadísticas de variables de entrada:")
    variables = ['participacion', 'puntualidad', 'calidad_trabajos', 
                'autoevaluacion', 'colaboracion']
    print(students_df[variables].describe())
    
    # Guardar datos
    filepath = generator.save_to_csv(students_df, 'estudiantes_datos.csv')
    
    print(f"\nPrimeros 5 estudiantes:")
    print(students_df[['nombre', 'perfil'] + variables + ['calificacion_tradicional']].head())
    
    return students_df

if __name__ == "__main__":
    df = main()