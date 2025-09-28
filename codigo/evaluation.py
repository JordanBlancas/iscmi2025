"""
Evaluación y Comparación del Sistema
===================================

Este módulo evalúa el rendimiento del sistema de lógica difusa
y lo compara con métodos tradicionales de calificación.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

from fuzzy_assessment import FuzzyAssessmentSystem
from data_generator import StudentDataGenerator

class SystemEvaluator:
    """Evaluador del sistema de lógica difusa vs métodos tradicionales."""
    
    def __init__(self):
        """Inicializa el evaluador."""
        self.fuzzy_system = FuzzyAssessmentSystem()
        self.data_generator = StudentDataGenerator()
    
    def run_complete_evaluation(self, n_students: int = 100) -> Dict:
        """
        Ejecuta una evaluación completa del sistema.
        
        Args:
            n_students: Número de estudiantes para la evaluación
            
        Returns:
            Diccionario con resultados de la evaluación
        """
        print(f"Iniciando evaluación con {n_students} estudiantes...")
        
        # Generar datos
        print("1. Generando datos de estudiantes...")
        students_df = self.data_generator.generate_realistic_student_data(n_students)
        students_df = self.data_generator.generate_traditional_grades(students_df)
        
        # Evaluar con sistema difuso
        print("2. Evaluando con sistema difuso...")
        fuzzy_results = self.fuzzy_system.evaluate_class(students_df)
        
        # Combinar resultados
        combined_df = students_df.merge(
            fuzzy_results[['estudiante_id', 'calificacion_fuzzy']], 
            on='estudiante_id'
        )
        
        # Calcular métricas
        print("3. Calculando métricas de comparación...")
        metrics = self.calculate_comparison_metrics(combined_df)
        
        # Generar visualizaciones
        print("4. Generando visualizaciones...")
        self.create_comparison_plots(combined_df, save_plots=True)
        
        # Guardar resultados
        self.data_generator.save_to_csv(combined_df, 'resultados_evaluacion.csv')
        
        print("✅ Evaluación completada")
        return {
            'data': combined_df,
            'metrics': metrics,
            'summary': self.generate_summary_report(combined_df, metrics)
        }
    
    def calculate_comparison_metrics(self, df: pd.DataFrame) -> Dict:
        """Calcula métricas de comparación entre sistemas."""
        metrics = {}
        
        # Correlaciones
        metrics['correlation_traditional_fuzzy'] = df['calificacion_tradicional'].corr(
            df['calificacion_fuzzy']
        )
        
        # Estadísticas descriptivas
        metrics['traditional_stats'] = {
            'mean': df['calificacion_tradicional'].mean(),
            'std': df['calificacion_tradicional'].std(),
            'min': df['calificacion_tradicional'].min(),
            'max': df['calificacion_tradicional'].max()
        }
        
        metrics['fuzzy_stats'] = {
            'mean': df['calificacion_fuzzy'].mean(),
            'std': df['calificacion_fuzzy'].std(),
            'min': df['calificacion_fuzzy'].min(),
            'max': df['calificacion_fuzzy'].max()
        }
        
        # Test de normalidad
        _, p_traditional = stats.shapiro(df['calificacion_tradicional'])
        _, p_fuzzy = stats.shapiro(df['calificacion_fuzzy'])
        
        metrics['normality_tests'] = {
            'traditional_is_normal': p_traditional > 0.05,
            'fuzzy_is_normal': p_fuzzy > 0.05,
            'traditional_p_value': p_traditional,
            'fuzzy_p_value': p_fuzzy
        }
        
        # Test t para diferencia de medias
        t_stat, t_p_value = stats.ttest_rel(
            df['calificacion_tradicional'], 
            df['calificacion_fuzzy']
        )
        
        metrics['mean_difference_test'] = {
            't_statistic': t_stat,
            'p_value': t_p_value,
            'significant_difference': t_p_value < 0.05
        }
        
        # Análisis por perfil de estudiante
        metrics['by_profile'] = {}
        for perfil in df['perfil'].unique():
            subset = df[df['perfil'] == perfil]
            metrics['by_profile'][perfil] = {
                'count': len(subset),
                'traditional_mean': subset['calificacion_tradicional'].mean(),
                'fuzzy_mean': subset['calificacion_fuzzy'].mean(),
                'difference': subset['calificacion_fuzzy'].mean() - subset['calificacion_tradicional'].mean()
            }
        
        return metrics
    
    def create_comparison_plots(self, df: pd.DataFrame, save_plots: bool = False):
        """Crea visualizaciones comparativas."""
        # Configurar estilo
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Crear figura con subplots
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Distribución de calificaciones
        ax1 = plt.subplot(2, 3, 1)
        df[['calificacion_tradicional', 'calificacion_fuzzy']].hist(
            bins=15, alpha=0.7, ax=ax1
        )
        ax1.set_title('Distribución de Calificaciones')
        ax1.set_xlabel('Calificación')
        ax1.set_ylabel('Frecuencia')
        ax1.legend(['Tradicional', 'Lógica Difusa'])
        ax1.grid(True, alpha=0.3)
        
        # 2. Scatter plot comparativo
        ax2 = plt.subplot(2, 3, 2)
        scatter = ax2.scatter(
            df['calificacion_tradicional'], 
            df['calificacion_fuzzy'],
            c=df['perfil'].astype('category').cat.codes,
            alpha=0.6,
            s=50
        )
        ax2.plot([0, 20], [0, 20], 'r--', alpha=0.8, linewidth=2)
        ax2.set_xlabel('Calificación Tradicional')
        ax2.set_ylabel('Calificación Lógica Difusa')
        ax2.set_title('Comparación de Calificaciones')
        ax2.grid(True, alpha=0.3)
        
        # Agregar línea de tendencia
        z = np.polyfit(df['calificacion_tradicional'], df['calificacion_fuzzy'], 1)
        p = np.poly1d(z)
        ax2.plot(df['calificacion_tradicional'], p(df['calificacion_tradicional']), 
                "b--", alpha=0.8, linewidth=2)
        
        # 3. Box plot por perfil
        ax3 = plt.subplot(2, 3, 3)
        df_melted = pd.melt(
            df, 
            id_vars=['perfil'], 
            value_vars=['calificacion_tradicional', 'calificacion_fuzzy'],
            var_name='Método', 
            value_name='Calificación'
        )
        sns.boxplot(data=df_melted, x='perfil', y='Calificación', hue='Método', ax=ax3)
        ax3.set_title('Calificaciones por Perfil de Estudiante')
        ax3.tick_params(axis='x', rotation=45)
        
        # 4. Diferencias por estudiante
        ax4 = plt.subplot(2, 3, 4)
        diferencias = df['calificacion_fuzzy'] - df['calificacion_tradicional']
        ax4.hist(diferencias, bins=20, alpha=0.7, color='green')
        ax4.axvline(diferencias.mean(), color='red', linestyle='--', 
                   label=f'Media: {diferencias.mean():.2f}')
        ax4.set_xlabel('Diferencia (Difusa - Tradicional)')
        ax4.set_ylabel('Frecuencia')
        ax4.set_title('Distribución de Diferencias')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # 5. Correlación entre variables de entrada
        ax5 = plt.subplot(2, 3, 5)
        variables_entrada = ['participacion', 'puntualidad', 'calidad_trabajos', 
                           'autoevaluacion', 'colaboracion']
        correlation_matrix = df[variables_entrada].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', 
                   center=0, ax=ax5, square=True)
        ax5.set_title('Correlación entre Variables de Entrada')
        
        # 6. Análisis de fairness
        ax6 = plt.subplot(2, 3, 6)
        fairness_data = []
        for perfil in df['perfil'].unique():
            subset = df[df['perfil'] == perfil]
            fairness_data.append({
                'Perfil': perfil,
                'Método': 'Tradicional',
                'Calificación': subset['calificacion_tradicional'].mean(),
                'Std': subset['calificacion_tradicional'].std()
            })
            fairness_data.append({
                'Perfil': perfil,
                'Método': 'Lógica Difusa',
                'Calificación': subset['calificacion_fuzzy'].mean(),
                'Std': subset['calificacion_fuzzy'].std()
            })
        
        fairness_df = pd.DataFrame(fairness_data)
        fairness_pivot = fairness_df.pivot(index='Perfil', columns='Método', values='Calificación')
        fairness_pivot.plot(kind='bar', ax=ax6, width=0.8)
        ax6.set_title('Promedio de Calificaciones por Perfil')
        ax6.set_ylabel('Calificación Promedio')
        ax6.tick_params(axis='x', rotation=45)
        ax6.legend()
        
        plt.tight_layout()
        
        if save_plots:
            plt.savefig('/workspaces/iscmi2025/figuras/comparacion_sistemas.png', 
                       dpi=300, bbox_inches='tight')
            print("Gráficos guardados en: /workspaces/iscmi2025/figuras/comparacion_sistemas.png")
        
        plt.show()
    
    def generate_summary_report(self, df: pd.DataFrame, metrics: Dict) -> str:
        """Genera un reporte resumen de la evaluación."""
        report = []
        report.append("="*60)
        report.append("REPORTE DE EVALUACIÓN DEL SISTEMA DE LÓGICA DIFUSA")
        report.append("="*60)
        
        report.append(f"\n📊 DATOS GENERALES:")
        report.append(f"• Total de estudiantes evaluados: {len(df)}")
        report.append(f"• Distribución por perfil:")
        for perfil, count in df['perfil'].value_counts().items():
            report.append(f"  - {perfil}: {count} estudiantes ({count/len(df)*100:.1f}%)")
        
        report.append(f"\n📈 ESTADÍSTICAS COMPARATIVAS:")
        trad_stats = metrics['traditional_stats']
        fuzzy_stats = metrics['fuzzy_stats']
        
        report.append(f"• Método Tradicional:")
        report.append(f"  - Promedio: {trad_stats['mean']:.2f} ± {trad_stats['std']:.2f}")
        report.append(f"  - Rango: [{trad_stats['min']:.2f}, {trad_stats['max']:.2f}]")
        
        report.append(f"• Lógica Difusa:")
        report.append(f"  - Promedio: {fuzzy_stats['mean']:.2f} ± {fuzzy_stats['std']:.2f}")
        report.append(f"  - Rango: [{fuzzy_stats['min']:.2f}, {fuzzy_stats['max']:.2f}]")
        
        report.append(f"\n🔗 CORRELACIÓN:")
        corr = metrics['correlation_traditional_fuzzy']
        report.append(f"• Correlación entre métodos: {corr:.3f}")
        if corr > 0.7:
            report.append("  ✅ Alta correlación - Los métodos son consistentes")
        elif corr > 0.5:
            report.append("  ⚠️  Correlación moderada - Diferencias notables")
        else:
            report.append("  ❌ Baja correlación - Métodos muy diferentes")
        
        report.append(f"\n📋 ANÁLISIS POR PERFIL:")
        for perfil, data in metrics['by_profile'].items():
            diff = data['difference']
            report.append(f"• {perfil.title()}:")
            report.append(f"  - Tradicional: {data['traditional_mean']:.2f}")
            report.append(f"  - Lógica Difusa: {data['fuzzy_mean']:.2f}")
            report.append(f"  - Diferencia: {diff:+.2f}")
            
            if abs(diff) < 0.5:
                report.append("    → Métodos muy similares")
            elif diff > 0:
                report.append("    → Lógica difusa califica más alto")
            else:
                report.append("    → Método tradicional califica más alto")
        
        report.append(f"\n🎯 CONCLUSIONES:")
        
        # Análisis de diferencia significativa
        mean_diff_test = metrics['mean_difference_test']
        if mean_diff_test['significant_difference']:
            report.append("• Existe diferencia significativa entre los métodos")
        else:
            report.append("• No hay diferencia significativa entre los métodos")
        
        # Recomendaciones
        report.append(f"\n💡 RECOMENDACIONES:")
        if corr > 0.6:
            report.append("• Los sistemas son complementarios")
            report.append("• Se puede usar lógica difusa para refinar evaluaciones tradicionales")
        
        if fuzzy_stats['std'] < trad_stats['std']:
            report.append("• La lógica difusa reduce la variabilidad en calificaciones")
            report.append("• Potencialmente más justo para estudiantes")
        
        report.append("="*60)
        
        return "\n".join(report)

def main():
    """Función principal para ejecutar la evaluación."""
    evaluator = SystemEvaluator()
    results = evaluator.run_complete_evaluation(n_students=80)
    
    # Mostrar reporte
    print("\n" + results['summary'])
    
    return results

if __name__ == "__main__":
    results = main()