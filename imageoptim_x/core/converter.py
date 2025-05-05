import os
import rawpy
import imageio
import numpy as np
from PIL import Image

def convert_raw_to_jpeg(raw_path, output_path, quality=82, preserve_metadata=True):
    """
    RAW DNGファイルをJPEGに変換する関数
    
    Parameters:
    raw_path (str): 処理するRAWファイルのパス
    output_path (str): 出力するJPEGファイルのパス
    quality (int): JPEG変換時の品質（0-100）
    preserve_metadata (bool): メタデータを保持するかどうか
    
    Returns:
    dict: 処理結果の情報（元サイズ、新サイズ、削減率など）
    """
    try:
        # RAWファイルの処理
        with rawpy.imread(raw_path) as raw:
            # RAWデータの処理（基本的な現像設定）
            rgb = raw.postprocess(
                use_camera_wb=True,
                half_size=False,
                no_auto_bright=False,
                output_color=rawpy.ColorSpace.sRGB
            )
        
        # JPEGとして保存
        imageio.imsave(output_path, rgb, quality=quality)
        
        # 結果情報の収集
        original_size = os.path.getsize(raw_path)
        new_size = os.path.getsize(output_path)
        reduction_rate = (1 - new_size/original_size) * 100
        
        result = {
            'original_path': raw_path,
            'output_path': output_path,
            'original_size': original_size,
            'output_size': new_size,
            'reduction_rate': reduction_rate,
            'quality': quality
        }
        
        return result
        
    except Exception as e:
        raise RuntimeError(f"変換エラー: {str(e)}")