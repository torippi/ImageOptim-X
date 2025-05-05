import os
import pytest
import tempfile
import json
from PIL import Image
import piexif

from imageoptim_x.core.converter import convert_raw_to_jpeg
from imageoptim_x.core.metadata import extract_raw_metadata, apply_metadata_to_jpeg

class TestMetadata:
    """メタデータ処理機能のテストクラス"""
    
    # テスト用のサンプルDNGファイルのパス
    SAMPLE_DNG = os.path.join(os.path.dirname(__file__), 'data', 'sample.dng')
    
    def test_extract_raw_metadata(self):
        """RAWメタデータ抽出のテスト"""
        # テスト前の確認
        if not os.path.exists(self.SAMPLE_DNG):
            pytest.skip("テスト用のサンプルDNGファイルが見つかりません")
        
        # メタデータの抽出
        metadata = extract_raw_metadata(self.SAMPLE_DNG)
        
        # 基本的なメタデータが存在するか検証
        assert isinstance(metadata, dict), "抽出されたメタデータが辞書型ではありません"
        assert 'raw_type' in metadata, "RAWタイプが含まれていません"
        assert 'raw_width' in metadata, "画像幅が含まれていません"
        assert 'raw_height' in metadata, "画像高さが含まれていません"
    
    def test_apply_metadata_to_jpeg(self):
        """JPEGへのメタデータ適用テスト"""
        # テスト前の確認
        if not os.path.exists(self.SAMPLE_DNG):
            pytest.skip("テスト用のサンプルDNGファイルが見つかりません")
        
        # 一時ファイルの作成
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp:
            output_path = temp.name
        
        try:
            # RAWからJPEGへの変換
            convert_raw_to_jpeg(self.SAMPLE_DNG, output_path, quality=80)
            
            # メタデータの抽出と適用
            metadata = extract_raw_metadata(self.SAMPLE_DNG)
            result = apply_metadata_to_jpeg(output_path, metadata)
            
            # 結果検証
            assert result is True, "メタデータの適用に失敗しました"
            
            # JPEGファイルからメタデータを読み取って検証
            img = Image.open(output_path)
            
            # EXIFデータの確認
            has_exif = 'exif' in img.info
            assert has_exif, "JPEGにEXIFデータが含まれていません"
            
        finally:
            # テスト後のクリーンアップ
            if os.path.exists(output_path):
                os.unlink(output_path)