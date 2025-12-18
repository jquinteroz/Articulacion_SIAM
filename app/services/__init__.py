"""Servicios de la aplicación"""

from .auth_service import AuthService
from .documento_service import DocumentoService
from .matricula_service import MatriculaService
from .reporte_service import ReporteService

__all__ = [
    'AuthService',
    'DocumentoService',
    'MatriculaService',
    'ReporteService'
]
