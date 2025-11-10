import pandas as pd
import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import matplotlib.pyplot as plt
import io
import base64
from config import EXPORT_CONFIG

class ExportManager:
    def __init__(self):
        self.output_dir = EXPORT_CONFIG['output_dir']
        os.makedirs(self.output_dir, exist_ok=True)
        
    def export_to_csv(self, df, filename=None):
        """Exporta DataFrame a CSV"""
        if filename is None:
            filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(self.output_dir, filename)
        df.to_csv(filepath, index=False, encoding='utf-8')
        return filepath
    
    def export_to_excel(self, df, filename=None, sheet_name='Data'):
        """Exporta DataFrame a Excel con formato"""
        if filename is None:
            filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Formatear hoja
            worksheet = writer.sheets[sheet_name]
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        return filepath
    
    def export_to_json(self, df, filename=None):
        """Exporta DataFrame a JSON"""
        if filename is None:
            filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        df.to_json(filepath, orient='records', indent=2, force_ascii=False)
        return filepath
    
    def create_analysis_report(self, df, ml_results=None, charts=None, insights=None):
        """Crea reporte PDF completo de análisis"""
        filename = f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.darkblue
        )
        story.append(Paragraph("Reporte de Análisis de Datos", title_style))
        story.append(Spacer(1, 20))
        
        # Información del dataset
        story.append(Paragraph("Resumen del Dataset", styles['Heading2']))
        dataset_info = [
            ['Métrica', 'Valor'],
            ['Filas', f"{df.shape[0]:,}"],
            ['Columnas', f"{df.shape[1]:,}"],
            ['Valores faltantes', f"{df.isnull().sum().sum():,}"],
            ['Memoria (MB)', f"{df.memory_usage(deep=True).sum() / 1024**2:.2f}"],
            ['Fecha de análisis', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        ]
        
        table = Table(dataset_info)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Estadísticas descriptivas
        if len(df.select_dtypes(include=['number']).columns) > 0:
            story.append(Paragraph("Estadísticas Descriptivas", styles['Heading2']))
            desc_stats = df.describe().round(2)
            
            # Convertir a tabla
            stats_data = [['Estadística'] + list(desc_stats.columns)]
            for idx in desc_stats.index:
                row = [idx] + [f"{val:.2f}" if isinstance(val, (int, float)) else str(val) 
                              for val in desc_stats.loc[idx]]
                stats_data.append(row)
            
            stats_table = Table(stats_data)
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(stats_table)
            story.append(Spacer(1, 20))
        
        # Resultados ML
        if ml_results:
            story.append(Paragraph("Resultados de Machine Learning", styles['Heading2']))
            for algorithm, metrics in ml_results.items():
                if 'error' not in metrics:
                    story.append(Paragraph(f"<b>{algorithm}</b>", styles['Heading3']))
                    story.append(Paragraph(f"R² Score: {metrics.get('r2_score', 0):.3f}", styles['Normal']))
                    story.append(Paragraph(f"MAE: {metrics.get('mae', 0):.3f}", styles['Normal']))
                    story.append(Paragraph(f"CV Score: {metrics.get('cv_score', 0):.3f}", styles['Normal']))
                    story.append(Spacer(1, 10))
        
        # Insights de IA
        if insights:
            story.append(Paragraph("Insights de Inteligencia Artificial", styles['Heading2']))
            story.append(Paragraph(insights, styles['Normal']))
            story.append(Spacer(1, 20))
        
        # Construir PDF
        doc.build(story)
        return filepath
    
    def export_charts_to_images(self, figures, prefix="chart"):
        """Exporta gráficos matplotlib a imágenes"""
        image_paths = []
        
        for i, fig in enumerate(figures):
            filename = f"{prefix}_{i+1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(self.output_dir, filename)
            fig.savefig(filepath, dpi=300, bbox_inches='tight')
            image_paths.append(filepath)
        
        return image_paths
    
    def create_dashboard_data(self, df, ml_results=None):
        """Crea datos para dashboard web"""
        dashboard_data = {
            'dataset_info': {
                'shape': df.shape,
                'columns': list(df.columns),
                'dtypes': df.dtypes.to_dict(),
                'missing_values': df.isnull().sum().to_dict(),
                'memory_usage': df.memory_usage(deep=True).sum()
            },
            'statistics': df.describe().to_dict() if len(df.select_dtypes(include=['number']).columns) > 0 else {},
            'ml_results': ml_results or {},
            'timestamp': datetime.now().isoformat()
        }
        
        filename = f"dashboard_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(dashboard_data, f, indent=2, ensure_ascii=False, default=str)
        
        return filepath
    
    def get_export_history(self):
        """Obtiene historial de exportaciones"""
        files = []
        for filename in os.listdir(self.output_dir):
            filepath = os.path.join(self.output_dir, filename)
            if os.path.isfile(filepath):
                stat = os.stat(filepath)
                files.append({
                    'filename': filename,
                    'size': stat.st_size,
                    'created': datetime.fromtimestamp(stat.st_ctime),
                    'modified': datetime.fromtimestamp(stat.st_mtime)
                })
        
        return sorted(files, key=lambda x: x['modified'], reverse=True)