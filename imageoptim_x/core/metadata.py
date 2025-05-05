from PIL import Image
import piexif
import json
import os

def extract_raw_metadata(raw_path):
    """
    RAWファイルからメタデータを抽出する
    
    Parameters:
    raw_path (str): RAWファイルのパス
    
    Returns:
    dict: 抽出されたメタデータ
    """
    import rawpy
    
    metadata = {}
    
    try:
        with rawpy.imread(raw_path) as raw:
            # カメラモデル
            if hasattr(raw, 'camera_model') and raw.camera_model:
                metadata['camera_model'] = raw.camera_model
            
            # 基本的なRAWファイル情報
            metadata['raw_type'] = os.path.splitext(raw_path)[1][1:].upper()
            metadata['raw_height'] = raw.sizes.raw_height
            metadata['raw_width'] = raw.sizes.raw_width
            
            # その他利用可能なメタデータ
            # 実際の実装ではrawpyからより多くのメタデータを抽出
    
    except Exception as e:
        print(f"メタデータ抽出エラー: {str(e)}")
    
    return metadata

def apply_metadata_to_jpeg(jpeg_path, metadata_dict):
    """
    JPEGファイルにメタデータを適用する
    
    Parameters:
    jpeg_path (str): JPEGファイルのパス
    metadata_dict (dict): 適用するメタデータの辞書
    
    Returns:
    bool: 成功したかどうか
    """
    try:
        # PILでイメージを開く
        img = Image.open(jpeg_path)
        
        # 既存のEXIFデータがあれば取得
        exif_dict = {"0th":{}, "Exif":{}, "GPS":{}, "1st":{}, "thumbnail":None}
        
        try:
            if 'exif' in img.info:
                exif_dict = piexif.load(img.info['exif'])
        except:
            pass
        
        # メタデータをEXIFに変換して適用
        # 実際には、metadata_dictのキーをEXIFタグにマッピングする必要がある
        
        # メタデータを適用して保存
        exif_bytes = piexif.dump(exif_dict)
        img.save(jpeg_path, exif=exif_bytes)
        
        return True
    
    except Exception as e:
        print(f"メタデータ適用エラー: {str(e)}")
        return False