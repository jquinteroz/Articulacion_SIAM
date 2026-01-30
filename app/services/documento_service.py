from app.models import db, Documento
from app.utils.helpers import save_uploaded_file
from flask import current_app
import os

class DocumentoService:
    """Servicio para manejo de documentos"""

    @staticmethod
    def upload_documento(file, matricula, tipo_documento):
        """
        Carga un documento
        Returns: (success, message, documento)
        """
        try:
            aprendiz = matricula.aprendiz

            # Guardar el archivo
            file_path = save_uploaded_file(file, aprendiz, tipo_documento)
            if not file_path:
                return False, 'Error al guardar el archivo', None

            # Verificar si ya existe un documento de este tipo
            doc_existente = Documento.query.filter_by(
                matricula_id=matricula.id,
                tipo_documento=tipo_documento
            ).filter(Documento.reemplazado_por == None).first()

            if doc_existente:
                # Marcar el anterior como reemplazado
                nuevo_doc = Documento(
                    matricula_id=matricula.id,
                    tipo_documento=tipo_documento,
                    nombre_archivo=file.filename,
                    ruta_archivo=file_path,
                    tamaño_bytes=os.path.getsize(file_path),
                    extension=file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
                )
                db.session.add(nuevo_doc)
                db.session.flush()

                doc_existente.reemplazado_por = nuevo_doc.id
                documento = nuevo_doc
            else:
                # Crear nuevo documento
                documento = Documento(
                    matricula_id=matricula.id,
                    tipo_documento=tipo_documento,
                    nombre_archivo=file.filename,
                    ruta_archivo=file_path,
                    tamaño_bytes=os.path.getsize(file_path),
                    extension=file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
                )
                db.session.add(documento)

            db.session.commit()
            return True, 'Documento cargado exitosamente', documento

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al cargar documento: {e}")
            return False, f'Error al cargar documento: {str(e)}', None

    @staticmethod
    def replace_documento(documento_id, file, user_id):
        """Reemplaza un documento existente (usado por docentes)"""
        try:
            doc_original = Documento.query.get(documento_id)
            if not doc_original:
                return False, 'Documento no encontrado', None

            aprendiz = doc_original.matricula.aprendiz
            tipo_documento = doc_original.tipo_documento

            # Guardar el nuevo archivo
            file_path = save_uploaded_file(file, aprendiz, tipo_documento)
            if not file_path:
                return False, 'Error al guardar el archivo', None

            # Crear el nuevo documento
            nuevo_doc = Documento(
                matricula_id=doc_original.matricula_id,
                tipo_documento=tipo_documento,
                nombre_archivo=file.filename,
                ruta_archivo=file_path,
                tamaño_bytes=os.path.getsize(file_path),
                extension=file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else '',
                # Al crear un reemplazo debe quedar como pendiente de revisión
                validado=None
            )
            db.session.add(nuevo_doc)
            db.session.flush()

            # Marcar el anterior como reemplazado
            doc_original.reemplazado_por = nuevo_doc.id

            db.session.commit()
            return True, 'Documento reemplazado exitosamente', nuevo_doc

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al reemplazar documento: {e}")
            return False, f'Error al reemplazar documento: {str(e)}', None

    @staticmethod
    def validar_documento(documento_id, user_id, observaciones=None):
        """Valida un documento"""
        try:
            documento = Documento.query.get(documento_id)
            if not documento:
                return False, 'Documento no encontrado'

            documento.validado = True
            documento.validado_por = user_id
            documento.fecha_validacion = db.func.now()
            documento.observaciones = observaciones

            db.session.commit()
            return True, 'Documento validado exitosamente'

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al validar documento: {e}")
            return False, f'Error al validar documento: {str(e)}'

    @staticmethod
    def delete_documento(documento_id):
        """Elimina un documento"""
        try:
            documento = Documento.query.get(documento_id)
            if not documento:
                return False, 'Documento no encontrado'

            # Eliminar archivo físico
            if os.path.exists(documento.ruta_archivo):
                os.remove(documento.ruta_archivo)

            db.session.delete(documento)
            db.session.commit()
            return True, 'Documento eliminado exitosamente'

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al eliminar documento: {e}")
            return False, f'Error al eliminar documento: {str(e)}'

    @staticmethod
    def get_documentos_activos(matricula_id):
        """Obtiene los documentos activos de una matrícula (no reemplazados)"""
        return Documento.query.filter_by(
            matricula_id=matricula_id
        ).filter(Documento.reemplazado_por == None).all()
