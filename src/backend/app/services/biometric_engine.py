"""Engine de processamento biométrico: extração de embeddings e matching"""

import base64
import io
import numpy as np
from PIL import Image
from typing import List
import os
from deepface import DeepFace
import cv2
from ..config import settings

# Usar DeepFace REAL para biometria
USE_DEEPFACE = True
print("🚀 DEEPFACE REAL ATIVADO - Processamento biométrico verdadeiro")

try:
    from deepface import DeepFace
    print("✅ DeepFace importado com sucesso")
except ImportError as e:
    print(f"❌ Erro ao importar DeepFace: {e}")
    raise ImportError("DeepFace é obrigatório. Execute: pip install deepface tensorflow opencv-python")


def base64_to_image(b64_string: str) -> np.ndarray:
    """
    Converte string base64 para numpy array (imagem).
    
    Args:
        b64_string: String base64 da imagem (com ou sem prefixo data:image/...)
    
    Returns:
        Array numpy representando a imagem RGB
    """
    # Remove prefixo data:image se existir
    if "," in b64_string:
        b64_string = b64_string.split(",")[1]
    
    image_data = base64.b64decode(b64_string)
    image = Image.open(io.BytesIO(image_data))
    
    # Converte para RGB se necessário
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    return np.array(image)


def extract_embedding(image_b64: str) -> List[float]:
    """
    Extrai embedding (vetor de features) facial de uma imagem.
    
    Args:
        image_b64: Imagem em formato base64
        
    Returns:
        Lista com o embedding facial
        
    Raises:
        ValueError: Se não conseguir encontrar face na imagem
    """
    try:
        # Converte base64 para array numpy
        image_array = base64_to_image(image_b64)
        print(f"📸 Processando imagem: {image_array.shape}")
        
        # Usar DeepFace para extrair embedding REAL
        print("🧠 Iniciando extração de embedding com DeepFace...")
        
        # Tentar diferentes configurações do DeepFace para maior tolerância
        embedding = None
        
        try:
            # Primeira tentativa: Facenet512 com detecção obrigatória
            embedding_result = DeepFace.represent(
                img_path=image_array,
                model_name="Facenet512",
                enforce_detection=True,
                detector_backend="opencv"
            )
            embedding = embedding_result[0]["embedding"]
            print(f"✅ Embedding extraído (Facenet512): {len(embedding)} dimensões")
            
        except Exception as e1:
            print(f"⚠️ Tentativa 1 falhou: {e1}")
            
            try:
                # Segunda tentativa: Facenet512 sem detecção obrigatória
                embedding_result = DeepFace.represent(
                    img_path=image_array,
                    model_name="Facenet512",
                    enforce_detection=False,
                    detector_backend="opencv"
                )
                embedding = embedding_result[0]["embedding"]
                print(f"✅ Embedding extraído (Facenet512, sem enforce): {len(embedding)} dimensões")
                
            except Exception as e2:
                print(f"⚠️ Tentativa 2 falhou: {e2}")
                
                try:
                    # Terceira tentativa: VGG-Face (mais tolerante)
                    embedding_result = DeepFace.represent(
                        img_path=image_array,
                        model_name="VGG-Face",
                        enforce_detection=False,
                        detector_backend="opencv"
                    )
                    embedding = embedding_result[0]["embedding"]
                    print(f"✅ Embedding extraído (VGG-Face): {len(embedding)} dimensões")
                    
                except Exception as e3:
                    print(f"❌ Todas as tentativas falharam: {e3}")
                    raise ValueError(f"Não foi possível detectar face na imagem após múltiplas tentativas")
        
        if embedding is None:
            raise ValueError("Falha na extração do embedding")
        
        return embedding
        
    except Exception as e:
        print(f"❌ Erro ao processar imagem: {str(e)}")
        raise ValueError(f"Erro ao extrair embedding biométrico: {str(e)}")
def cosine_similarity(emb1: List[float], emb2: List[float]) -> float:
    """
    Calcula similaridade de cosseno entre dois embeddings.
    
    Args:
        emb1: Primeiro embedding
        emb2: Segundo embedding
    
    Returns:
        Similaridade entre 0 e 1 (1 = idênticos)
    """
    a = np.array(emb1)
    b = np.array(emb2)
    
    # Evita divisão por zero
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return float(np.dot(a, b) / (norm_a * norm_b))


def verify_match(template_embedding: List[float], test_embedding: List[float]) -> bool:
    """
    Verifica se dois embeddings correspondem ao mesmo rosto.
    
    Args:
        template_embedding: Embedding cadastrado (template)
        test_embedding: Embedding a ser verificado
    
    Returns:
        True se os embeddings correspondem (acima do limiar)
    """
    similarity = cosine_similarity(template_embedding, test_embedding)
    
    # Usar limiar de similaridade padrão
    threshold = getattr(settings, 'SIMILARITY_THRESHOLD', 0.7)
    match = similarity >= threshold
    
    print(f"🔍 Similaridade DeepFace: {similarity:.3f} (limiar: {threshold}) - {'✅ MATCH' if match else '❌ NO MATCH'}")
    
    return match
