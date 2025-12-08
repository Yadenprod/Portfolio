from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import tempfile
import logging
from typing import Optional, Dict
import json
import asyncio
from pathlib import Path

from .solver import CaptchaSolver

logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """Создание FastAPI приложения"""
    
    app = FastAPI(
        title="CaptchaSolver API",
        description="Мощная система для распознавания капчи с множественными подходами",
        version="1.0.0"
    )
    
    # Инициализация решателя капчи
    solver = None
    
    @app.on_event("startup")
    async def startup_event():
        nonlocal solver
        try:
            solver = CaptchaSolver()
            logger.info("CaptchaSolver инициализирован успешно")
        except Exception as e:
            logger.error(f"Ошибка инициализации CaptchaSolver: {e}")
            raise
    
    @app.get("/", response_class=HTMLResponse)
    async def main_page():
        """Главная страница с интерфейсом"""
        html_content = """
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>CaptchaSolver - Распознавание капчи</title>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }
                
                .container {
                    background: white;
                    border-radius: 20px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    padding: 40px;
                    max-width: 800px;
                    width: 100%;
                }
                
                .header {
                    text-align: center;
                    margin-bottom: 40px;
                }
                
                .header h1 {
                    color: #333;
                    font-size: 2.5em;
                    margin-bottom: 10px;
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }
                
                .header p {
                    color: #666;
                    font-size: 1.2em;
                }
                
                .upload-section {
                    background: #f8f9fa;
                    border-radius: 15px;
                    padding: 30px;
                    margin-bottom: 30px;
                    border: 2px dashed #dee2e6;
                    transition: all 0.3s ease;
                }
                
                .upload-section:hover {
                    border-color: #667eea;
                    background: #f0f4ff;
                }
                
                .file-input-wrapper {
                    position: relative;
                    overflow: hidden;
                    display: inline-block;
                    cursor: pointer;
                    width: 100%;
                }
                
                .file-input {
                    position: absolute;
                    left: -9999px;
                    opacity: 0;
                }
                
                .file-input-button {
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                    padding: 15px 30px;
                    border-radius: 10px;
                    cursor: pointer;
                    display: block;
                    text-align: center;
                    font-size: 1.1em;
                    font-weight: 600;
                    transition: all 0.3s ease;
                    border: none;
                    width: 100%;
                }
                
                .file-input-button:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
                }
                
                .options {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 20px;
                    margin-bottom: 30px;
                }
                
                .option {
                    display: flex;
                    align-items: center;
                    background: #f8f9fa;
                    padding: 15px;
                    border-radius: 10px;
                }
                
                .option input[type="checkbox"] {
                    margin-right: 10px;
                    transform: scale(1.2);
                }
                
                .solve-button {
                    background: linear-gradient(135deg, #28a745, #20c997);
                    color: white;
                    padding: 15px 40px;
                    border: none;
                    border-radius: 10px;
                    font-size: 1.2em;
                    font-weight: 600;
                    cursor: pointer;
                    width: 100%;
                    transition: all 0.3s ease;
                }
                
                .solve-button:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 10px 20px rgba(40, 167, 69, 0.3);
                }
                
                .solve-button:disabled {
                    background: #6c757d;
                    cursor: not-allowed;
                    transform: none;
                    box-shadow: none;
                }
                
                .results {
                    margin-top: 30px;
                    padding: 20px;
                    background: #f8f9fa;
                    border-radius: 15px;
                    display: none;
                }
                
                .result-item {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 10px;
                    margin: 5px 0;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                
                .final-result {
                    background: linear-gradient(135deg, #28a745, #20c997);
                    color: white;
                    font-size: 1.5em;
                    font-weight: bold;
                    text-align: center;
                    padding: 20px;
                    border-radius: 15px;
                    margin-bottom: 20px;
                }
                
                .loading {
                    display: none;
                    text-align: center;
                    margin: 20px 0;
                }
                
                .spinner {
                    border: 4px solid #f3f3f3;
                    border-top: 4px solid #667eea;
                    border-radius: 50%;
                    width: 40px;
                    height: 40px;
                    animation: spin 2s linear infinite;
                    margin: 0 auto 10px;
                }
                
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                
                .image-preview {
                    max-width: 100%;
                    max-height: 200px;
                    border-radius: 10px;
                    margin: 20px 0;
                    display: none;
                }
                
                @media (max-width: 768px) {
                    .options {
                        grid-template-columns: 1fr;
                    }
                    
                    .container {
                        padding: 20px;
                    }
                    
                    .header h1 {
                        font-size: 2em;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔓 CaptchaSolver</h1>
                    <p>Мощная система распознавания капчи с ИИ</p>
                </div>
                
                <form id="captchaForm" enctype="multipart/form-data">
                    <div class="upload-section">
                        <div class="file-input-wrapper">
                            <input type="file" id="fileInput" name="file" accept="image/*" class="file-input" required>
                            <label for="fileInput" class="file-input-button">
                                📁 Выберите изображение капчи
                            </label>
                        </div>
                        <img id="imagePreview" class="image-preview" alt="Предпросмотр">
                    </div>
                    
                    <div class="options">
                        <div class="option">
                            <input type="checkbox" id="preprocessing" name="preprocessing" checked>
                            <label for="preprocessing">Использовать предобработку</label>
                        </div>
                        <div class="option">
                            <input type="checkbox" id="showSteps" name="show_steps">
                            <label for="showSteps">Показать этапы обработки</label>
                        </div>
                        <div class="option">
                            <input type="checkbox" id="consensus" name="consensus" checked>
                            <label for="consensus">Использовать консенсус</label>
                        </div>
                        <div class="option">
                            <input type="checkbox" id="benchmark" name="benchmark">
                            <label for="benchmark">Режим бенчмарка</label>
                        </div>
                    </div>
                    
                    <button type="submit" class="solve-button" id="solveButton">
                        🚀 Распознать капчу
                    </button>
                </form>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Анализируем изображение...</p>
                </div>
                
                <div class="results" id="results"></div>
            </div>
            
            <script>
                const form = document.getElementById('captchaForm');
                const fileInput = document.getElementById('fileInput');
                const imagePreview = document.getElementById('imagePreview');
                const loading = document.getElementById('loading');
                const results = document.getElementById('results');
                const solveButton = document.getElementById('solveButton');
                
                // Предпросмотр изображения
                fileInput.addEventListener('change', function(e) {
                    const file = e.target.files[0];
                    if (file) {
                        const reader = new FileReader();
                        reader.onload = function(e) {
                            imagePreview.src = e.target.result;
                            imagePreview.style.display = 'block';
                        };
                        reader.readAsDataURL(file);
                        
                        // Обновляем текст кнопки
                        document.querySelector('.file-input-button').textContent = `📁 ${file.name}`;
                    }
                });
                
                // Отправка формы
                form.addEventListener('submit', async function(e) {
                    e.preventDefault();
                    
                    const formData = new FormData();
                    const file = fileInput.files[0];
                    
                    if (!file) {
                        alert('Пожалуйста, выберите файл');
                        return;
                    }
                    
                    formData.append('file', file);
                    formData.append('use_preprocessing', document.getElementById('preprocessing').checked);
                    formData.append('show_steps', document.getElementById('showSteps').checked);
                    formData.append('use_consensus', document.getElementById('consensus').checked);
                    
                    // Показываем загрузку
                    loading.style.display = 'block';
                    results.style.display = 'none';
                    solveButton.disabled = true;
                    
                    try {
                        const response = await fetch('/solve', {
                            method: 'POST',
                            body: formData
                        });
                        
                        if (!response.ok) {
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }
                        
                        const result = await response.json();
                        displayResults(result);
                        
                    } catch (error) {
                        console.error('Error:', error);
                        alert('Произошла ошибка при обработке изображения');
                    } finally {
                        loading.style.display = 'none';
                        solveButton.disabled = false;
                    }
                });
                
                function displayResults(data) {
                    const resultsDiv = document.getElementById('results');
                    
                    const resultText = data.success ? data.text : 'Не удалось распознать';
                    const resultClass = data.success ? 'success' : 'error';
                    
                    let html = `
                        <div class="final-result ${resultClass}">
                            ${data.success ? '🎯' : '❌'} Результат: ${resultText}
                        </div>
                        
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px;">
                            <div class="result-item">
                                <span>⏱️ Время обработки:</span>
                                <strong>${data.processing_time?.toFixed(2) || 0} сек</strong>
                            </div>
                            <div class="result-item">
                                <span>🔧 Предобработка:</span>
                                <strong>Включена</strong>
                            </div>
                        </div>
                        
                        <h3 style="margin-bottom: 15px; color: #333;">📊 Результаты по методам:</h3>
                    `;
                    
                    const methodNames = {
                        'easyocr_original': '👁️ EasyOCR (оригинал)',
                        'easyocr_processed': '👁️ EasyOCR (обработанное)',
                        'easyocr_enlarged': '👁️ EasyOCR (увеличенное)',
                        'easyocr_binary': '👁️ EasyOCR (бинарное)',
                        'easyocr_otsu': '👁️ EasyOCR (OTSU)',
                        'easyocr_otsu_inv': '👁️ EasyOCR (OTSU инв.)',
                        'paddleocr': '🐼 PaddleOCR',
                        'custom_cnn': '🧠 CNN модель'
                    };
                    
                    for (const [method, result] of Object.entries(data.methods || {})) {
                        const methodName = methodNames[method] || method;
                        const methodText = result.text || '';
                        const confidence = result.confidence || 0;
                        const success = methodText === data.text && data.success;
                        
                        html += `
                            <div class="result-item" style="background: ${success ? '#d4edda' : '#fff'};">
                                <span>${methodName}:</span>
                                <strong style="color: ${success ? '#155724' : '#333'};">
                                    ${methodText || 'Ошибка'} ${success ? '✅' : ''}
                                </strong>
                            </div>
                        `;
                    }
                    
                    resultsDiv.innerHTML = html;
                    resultsDiv.style.display = 'block';
                }
            </script>
        </body>
        </html>
        """
        return html_content
    
    @app.post("/solve")
    async def solve_captcha(
        file: UploadFile = File(...),
        use_preprocessing: bool = Form(True),
        show_steps: bool = Form(False),
        use_consensus: bool = Form(True)
    ):
        """Решение капчи через API"""
        
        if solver is None:
            raise HTTPException(status_code=500, detail="Solver не инициализирован")
        
        # Проверяем тип файла
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Файл должен быть изображением")
        
        # Сохраняем временный файл
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                content = await file.read()
                tmp_file.write(content)
                tmp_file_path = tmp_file.name
            
            # Решаем капчу
            result = solver.solve(
                tmp_file_path,
                save_debug=show_steps
            )
            
            return JSONResponse(content=result)
            
        except Exception as e:
            logger.error(f"Ошибка при решении капчи: {e}")
            raise HTTPException(status_code=500, detail=f"Ошибка обработки: {str(e)}")
        
        finally:
            # Удаляем временный файл
            try:
                os.unlink(tmp_file_path)
            except:
                pass
    
    @app.get("/stats")
    async def get_stats():
        """Получение статистики работы"""
        if solver is None:
            raise HTTPException(status_code=500, detail="Solver не инициализирован")
        
        return JSONResponse(content=solver.get_stats())
    
    @app.post("/train")
    async def train_model(
        epochs: int = Form(50),
        use_synthetic: bool = Form(True)
    ):
        """Обучение собственной модели"""
        if solver is None:
            raise HTTPException(status_code=500, detail="Solver не инициализирован")
        
        try:
            # Запускаем обучение в фоне
            await asyncio.get_event_loop().run_in_executor(
                None, solver.train_custom_model, None, epochs, use_synthetic
            )
            
            return JSONResponse(content={"status": "success", "message": "Обучение завершено"})
            
        except Exception as e:
            logger.error(f"Ошибка обучения: {e}")
            raise HTTPException(status_code=500, detail=f"Ошибка обучения: {str(e)}")
    
    @app.get("/health")
    async def health_check():
        """Проверка здоровья сервиса"""
        return {
            "status": "healthy",
            "solver_initialized": solver is not None,
            "version": "1.0.0"
        }
    
    return app

def run_server(host: str = "127.0.0.1", port: int = 8000, debug: bool = False):
    """Запуск сервера"""
    app = create_app()
    
    logger.info(f"Запуск сервера на http://{host}:{port}")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="debug" if debug else "info",
        reload=debug
    )

if __name__ == "__main__":
    run_server(debug=True)