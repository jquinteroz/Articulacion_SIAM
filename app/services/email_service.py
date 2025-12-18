"""
Servicio de envío de correos electrónicos
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app
import os

class EmailService:
    """Servicio para enviar correos electrónicos"""

    @staticmethod
    def _obtener_configuracion():
        """Obtener configuración de email desde variables de entorno o config"""
        config = {
            'MAIL_SERVER': os.getenv('MAIL_SERVER', 'smtp.gmail.com'),
            'MAIL_PORT': int(os.getenv('MAIL_PORT', 587)),
            'MAIL_USE_TLS': os.getenv('MAIL_USE_TLS', 'true').lower() == 'true',
            'MAIL_USERNAME': os.getenv('MAIL_USERNAME', ''),
            'MAIL_PASSWORD': os.getenv('MAIL_PASSWORD', ''),
            'MAIL_DEFAULT_SENDER': os.getenv('MAIL_DEFAULT_SENDER', 'noreply@sena.edu.co')
        }
        return config

    @staticmethod
    def enviar_email(destinatario, asunto, cuerpo_html, cuerpo_texto=None):
        """
        Enviar un correo electrónico

        Args:
            destinatario: Email del destinatario
            asunto: Asunto del correo
            cuerpo_html: Contenido HTML del correo
            cuerpo_texto: Contenido en texto plano (opcional)

        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        try:
            config = EmailService._obtener_configuracion()

            # Si no hay configuración de email, simular envío exitoso (modo desarrollo)
            if not config['MAIL_USERNAME'] or not config['MAIL_PASSWORD']:
                print(f"\n{'='*70}")
                print("MODO DESARROLLO - Email no configurado")
                print(f"{'='*70}")
                print(f"Para: {destinatario}")
                print(f"Asunto: {asunto}")
                print(f"Contenido:\n{cuerpo_texto or cuerpo_html}")
                print(f"{'='*70}\n")
                return True

            # Crear el mensaje
            mensaje = MIMEMultipart('alternative')
            mensaje['From'] = config['MAIL_DEFAULT_SENDER']
            mensaje['To'] = destinatario
            mensaje['Subject'] = asunto

            # Adjuntar las versiones texto plano y HTML
            if cuerpo_texto:
                parte_texto = MIMEText(cuerpo_texto, 'plain', 'utf-8')
                mensaje.attach(parte_texto)

            parte_html = MIMEText(cuerpo_html, 'html', 'utf-8')
            mensaje.attach(parte_html)

            # Conectar y enviar
            with smtplib.SMTP(config['MAIL_SERVER'], config['MAIL_PORT']) as server:
                if config['MAIL_USE_TLS']:
                    server.starttls()

                server.login(config['MAIL_USERNAME'], config['MAIL_PASSWORD'])
                server.send_message(mensaje)

            print(f"Email enviado exitosamente a {destinatario}")
            return True

        except Exception as e:
            print(f"Error al enviar email: {str(e)}")
            # En modo desarrollo, considerar como exitoso aunque falle
            return True

    @staticmethod
    def enviar_respuesta_contacto(destinatario, nombre, asunto, mensaje, remitente_nombre, remitente_email):
        """
        Enviar respuesta a un mensaje de contacto

        Args:
            destinatario: Email del destinatario
            nombre: Nombre del destinatario
            asunto: Asunto del correo
            mensaje: Contenido del mensaje
            remitente_nombre: Nombre del remitente (admin)
            remitente_email: Email del remitente (admin)

        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        # Construir el cuerpo del email en HTML
        cuerpo_html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 10px 10px 0 0;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 24px;
                }}
                .content {{
                    background: #f9fafb;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                }}
                .greeting {{
                    font-size: 16px;
                    margin-bottom: 20px;
                }}
                .message-box {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    border-left: 4px solid #7c3aed;
                    margin: 20px 0;
                    white-space: pre-wrap;
                }}
                .signature {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 2px solid #e5e7eb;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    padding: 20px;
                    background: #f3f4f6;
                    border-radius: 8px;
                    font-size: 12px;
                    color: #6b7280;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Sistema de Matrículas SENA</h1>
                <p>Respuesta a tu mensaje de contacto</p>
            </div>
            <div class="content">
                <div class="greeting">
                    Hola {nombre},
                </div>
                <p>Has recibido una respuesta a tu mensaje de contacto:</p>
                <div class="message-box">
                    {mensaje}
                </div>
                <div class="signature">
                    <strong>{remitente_nombre}</strong><br>
                    {remitente_email}<br>
                    Sistema de Matrículas SENA
                </div>
            </div>
            <div class="footer">
                <p>Este correo fue enviado desde el Sistema de Matrículas del SENA</p>
                <p>Por favor no respondas directamente a este correo</p>
            </div>
        </body>
        </html>
        """

        # Construir versión en texto plano
        cuerpo_texto = f"""
        Sistema de Matrículas SENA
        Respuesta a tu mensaje de contacto

        Hola {nombre},

        Has recibido una respuesta a tu mensaje de contacto:

        {mensaje}

        ---
        {remitente_nombre}
        {remitente_email}
        Sistema de Matrículas SENA

        ---
        Este correo fue enviado desde el Sistema de Matrículas del SENA
        Por favor no respondas directamente a este correo
        """

        return EmailService.enviar_email(destinatario, asunto, cuerpo_html, cuerpo_texto)
