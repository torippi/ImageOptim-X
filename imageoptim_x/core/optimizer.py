import numpy as np
from PIL import Image

def analyze_image_complexity(image_array):
    """
    画像の複雑さを分析して最適なJPEG品質を推定する
    
    Parameters:
    image_array (numpy.ndarray): 画像データの配列
    
    Returns:
    int: 推奨JPEG品質設定（0-100）
    """
    # 標準偏差を使って画像の複雑さを測定
    # 複雑さが高いほど、より高い品質設定が必要
    std_dev = np.std(image_array)
    
    # 複雑さに基づいた品質のマッピング
    # これは簡易的なアルゴリズムで、実際にはもっと洗練されたアプローチが必要
    if std_dev < 15:
        return 70  # 比較的単純な画像
    elif std_dev < 30:
        return 80  # 中程度の複雑さ
    elif std_dev < 45:
        return 85  # やや複雑な画像
    else:
        return 90  # 非常に複雑な画像

def determine_optimal_quality(raw_path, device_target=None):
    """
    RAWファイルを分析し、最適なJPEG品質設定を決定する
    
    Parameters:
    raw_path (str): RAWファイルのパス
    device_target (str, optional): 出力の対象デバイス（例：'iphone', 'ipad', 'display'）
    
    Returns:
    int: 最適なJPEG品質設定（0-100）
    """
    import rawpy
    
    # RAWファイルを読み込み
    with rawpy.imread(raw_path) as raw:
        # サムネイルとして小さめに処理して分析を高速化
        rgb = raw.postprocess(use_camera_wb=True, half_size=True)
    
    # 画像の複雑さに基づく品質の基本推定
    base_quality = analyze_image_complexity(rgb)
    
    # デバイスターゲットに基づく調整
    if device_target:
        device_target = device_target.lower()
        if device_target == 'iphone':
            # iPhoneの小さな画面では若干品質を下げても良い
            return max(65, base_quality - 10)
        elif device_target == 'ipad':
            # iPadは中程度
            return max(70, base_quality - 5)
        elif device_target == 'display':
            # 大画面ディスプレイ用は高品質
            return min(95, base_quality + 5)
    
    return base_quality