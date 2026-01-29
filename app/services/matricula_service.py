from app.models import db, Matricula, Aprendiz, Documento
from flask import current_app
from datetime import datetime

class MatriculaService:
    """Servicio para manejo de matrículas"""

    @staticmethod
    def get_or_create_matricula(aprendiz_id):
        """Obtiene o crea la matrícula de un aprendiz"""
        try:
            matricula = Matricula.query.filter_by(aprendiz_id=aprendiz_id).first()

            if not matricula:
                matricula = Matricula(aprendiz_id=aprendiz_id, estado='BORRADOR')
                db.session.add(matricula)
                db.session.commit()

            return matricula

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al obtener/crear matrícula: {e}")
            return None

    @staticmethod
    def update_aprendiz_data(aprendiz_id, **kwargs):
        """Actualiza los datos del aprendiz"""
        try:
            aprendiz = Aprendiz.query.get(aprendiz_id)
            if not aprendiz:
                return False, 'Aprendiz no encontrado'

            # Campos permitidos
            allowed_fields = [
                'direccion', 'ciudad', 'departamento',
                'acudiente_tipo_doc', 'acudiente_documento',
                'acudiente_nombres', 'acudiente_apellidos',
                'acudiente_telefono', 'acudiente_email',
                'colegio_id', 'grupo_id', 'programa_id'
            ]

            for field in allowed_fields:
                if field in kwargs:
                    setattr(aprendiz, field, kwargs[field])

            # Verificar si el perfil está completo
            aprendiz.perfil_completo = MatriculaService._check_perfil_completo(aprendiz)

            db.session.commit()
            return True, 'Datos actualizados exitosamente'

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al actualizar aprendiz: {e}")
            return False, f'Error al actualizar datos: {str(e)}'

    @staticmethod
    def _check_perfil_completo(aprendiz):
        """Verifica si el perfil del aprendiz está completo"""
        required_fields = [
            aprendiz.ciudad,
            aprendiz.acudiente_documento,
            aprendiz.acudiente_lugar_expedicion,
            aprendiz.acudiente_nombres,
            aprendiz.acudiente_apellidos,
            aprendiz.acudiente_direccion,
            aprendiz.acudiente_telefono,
            aprendiz.colegio_id,
            aprendiz.grupo_id,
            aprendiz.programa_id
        ]
        return all(required_fields)

    @staticmethod
    def enviar_matricula(matricula_id):
        """Envía la matrícula para validación"""
        try:
            matricula = Matricula.query.get(matricula_id)
            if not matricula:
                return False, 'Matrícula no encontrada'

            # Verificar que tenga todos los documentos
            if not matricula.tiene_todos_documentos():
                return False, 'Debe cargar todos los documentos obligatorios'

            # NOTA: Comentado temporalmente - El perfil se puede completar después
            # if not matricula.aprendiz.perfil_completo:
            #     return False, 'Debe completar todos los datos del formulario'

            matricula.estado = 'ENVIADO'
            matricula.fecha_envio = datetime.utcnow()

            db.session.commit()
            return True, 'Matrícula enviada exitosamente'

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al enviar matrícula: {e}")
            return False, f'Error al enviar matrícula: {str(e)}'

    @staticmethod
    def validar_matricula_docente(matricula_id, docente_id, estado, observaciones=None):
        """Valida la matrícula por parte del docente"""
        try:
            matricula = Matricula.query.get(matricula_id)
            if not matricula:
                return False, 'Matrícula no encontrada'

            matricula.estado = estado
            matricula.validado_por_docente = docente_id
            matricula.fecha_validacion_docente = datetime.utcnow()
            matricula.observaciones_docente = observaciones

            db.session.commit()
            return True, 'Matrícula validada exitosamente'

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al validar matrícula: {e}")
            return False, f'Error al validar matrícula: {str(e)}'

    @staticmethod
    def validar_matricula_admin(matricula_id, admin_id, estado, observaciones=None):
        """Valida la matrícula por parte del administrador"""
        try:
            matricula = Matricula.query.get(matricula_id)
            if not matricula:
                return False, 'Matrícula no encontrada'

            matricula.estado = estado
            matricula.validado_por_admin = admin_id
            matricula.fecha_validacion_admin = datetime.utcnow()
            matricula.observaciones_admin = observaciones

            db.session.commit()
            return True, 'Matrícula validada exitosamente'

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al validar matrícula: {e}")
            return False, f'Error al validar matrícula: {str(e)}'

    @staticmethod
    def delete_matricula(matricula_id):
        """Elimina una matrícula"""
        try:
            matricula = Matricula.query.get(matricula_id)
            if not matricula:
                return False, 'Matrícula no encontrada'

            db.session.delete(matricula)
            db.session.commit()
            return True, 'Matrícula eliminada exitosamente'

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al eliminar matrícula: {e}")
            return False, f'Error al eliminar matrícula: {str(e)}'
