import os
import glob

def ensure_directory_exists(directory_path):
    """
    ディレクトリが存在しない場合は作成する
    
    Parameters:
    directory_path (str): 確認/作成するディレクトリのパス
    
    Returns:
    bool: ディレクトリが既に存在したか、新規作成したか
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)
        return False
    return True

def find_raw_files(source_dir, extensions=None):
    """
    指定されたディレクトリからRAWファイルを検索する
    
    Parameters:
    source_dir (str): 検索するディレクトリのパス
    extensions (list): 検索する拡張子のリスト（デフォルトは.dng）
    
    Returns:
    list: 見つかったRAWファイルのパスのリスト
    """
    if extensions is None:
        extensions = ['.dng']
    
    files = []
    for ext in extensions:
        pattern = os.path.join(source_dir, f"*{ext}")
        files.extend(glob.glob(pattern))
    
    return files

def get_output_path(raw_path, output_dir, extension='.jpg'):
    """
    RAWファイルに対応する出力ファイルのパスを取得する
    
    Parameters:
    raw_path (str): RAWファイルのパス
    output_dir (str): 出力ディレクトリのパス
    extension (str): 出力ファイルの拡張子
    
    Returns:
    str: 出力ファイルのパス
    """
    filename = os.path.basename(raw_path)
    base_name = os.path.splitext(filename)[0]
    return os.path.join(output_dir, f"{base_name}{extension}")