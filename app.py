from flask import Flask, request, jsonify
import os
from datetime import datetime
import logging

app = Flask(__name__)

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simulación de base de datos en memoria
comments_db = []

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de verificación de salud"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'flask-comments-api',
        'version': '1.0.0'
    }), 200

@app.route('/comments', methods=['GET'])
def get_comments():
    """Obtener todos los comentarios"""
    try:
        return jsonify({
            'comments': comments_db,
            'total': len(comments_db)
        }), 200
    except Exception as e:
        logger.error(f"Error al obtener comentarios: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500
@app.route('/comments/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    """Obtener un comentario específico"""
    try:
        comment = next((c for c in comments_db if c['id'] == comment_id), None)
        
        if not comment:
            return jsonify({'error': 'Comentario no encontrado'}), 404
            
        return jsonify(comment), 200
        
    except Exception as e:
        logger.error(f"Error al obtener comentario {comment_id}: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)