import os
import pytest
import tempfile
from PIL import Image

from imageoptim_x.core.converter import convert_raw_to_jpeg

class TestConverter:
    """変換機能のテストクラス"""
    
    # テスト用のサンプルDNGファイルのパス
    # 実際のテストでは、tests/data ディレクトリにサンプルファイルを用意することを推奨
    SAMPLE_DNG = os.path.join(os.path.dirname(__file__), 'data', 'sample.DNG')
    
    def test_convert_raw_to_jpeg_basic(self):
        """基本的な変換機能のテスト"""
        # テスト前の確認
        if not os.path.exists(self.SAMPLE_DNG):
            pytest.skip("テスト用のサンプルDNGファイルが見つかりません")
        
        # 一時ファイルの作成
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp:
            output_path = temp.name
        
        try:
            # 変換実行
            result = convert_raw_to_jpeg(self.SAMPLE_DNG, output_path, quality=80)
            
            # 結果検証
            assert os.path.exists(output_path), "出力ファイルが作成されていません"
            assert result['original_path'] == self.SAMPLE_DNG, "元ファイルパスが正しくありません"
            assert result['output_path'] == output_path, "出力ファイルパスが正しくありません"
            assert result['original_size'] > 0, "元ファイルサイズが正しくありません"
            assert result['output_size'] > 0, "出力ファイルサイズが正しくありません"
            assert result['quality'] == 80, "品質設定が正しくありません"
            
            # 画像が正しく開けるか確認
            img = Image.open(output_path)
            assert img.format == 'JPEG', "出力が正しいJPEG形式ではありません"
            
        finally:
            # テスト後のクリーンアップ
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_convert_raw_to_jpeg_quality_settings(self):
        """異なる品質設定でのテスト"""
        if not os.path.exists(self.SAMPLE_DNG):
            pytest.skip("テスト用のサンプルDNGファイルが見つかりません")
        
        # 異なる品質設定でテスト
        qualities = [70, 85, 100]
        output_files = []
        file_sizes = []
        
        try:
            for quality in qualities:
                # 一時ファイルの作成
                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp:
                    output_path = temp.name
                    output_files.append(output_path)
                
                # 変換実行
                result = convert_raw_to_jpeg(self.SAMPLE_DNG, output_path, quality=quality)
                file_sizes.append(result['output_size'])
            
            # 品質が高いほど、ファイルサイズも大きくなることを検証
            # (これは一般的な傾向であり、画像によっては例外もある)
            assert file_sizes[0] <= file_sizes[1] <= file_sizes[2], "品質とファイルサイズの関係が想定と異なります"
            
        finally:
            # テスト後のクリーンアップ
            for path in output_files:
                if os.path.exists(path):
                    os.unlink(path)