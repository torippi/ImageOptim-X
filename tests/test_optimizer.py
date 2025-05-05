import os
import pytest
import numpy as np

from imageoptim_x.core.optimizer import analyze_image_complexity, determine_optimal_quality

class TestOptimizer:
    """最適化機能のテストクラス"""
    
    # テスト用のサンプルDNGファイルのパス
    SAMPLE_DNG = os.path.join(os.path.dirname(__file__), 'data', 'sample.dng')
    
    def test_analyze_image_complexity(self):
        """画像複雑性分析のテスト"""
        # 様々な複雑さの画像をシミュレート
        simple_image = np.ones((100, 100, 3), dtype=np.uint8) * 128  # グレーの単色画像
        medium_image = np.random.randint(100, 150, (100, 100, 3), dtype=np.uint8)  # 少し変化のある画像
        complex_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)  # ランダムな画像
        
        # 複雑さに応じた品質のテスト
        simple_quality = analyze_image_complexity(simple_image)
        medium_quality = analyze_image_complexity(medium_image)
        complex_quality = analyze_image_complexity(complex_image)
        
        # 複雑さが高いほど、高い品質設定になることを検証
        assert simple_quality <= medium_quality <= complex_quality, "画像の複雑さと品質の関係が想定と異なります"
    
    def test_determine_optimal_quality(self):
        """最適品質決定のテスト"""
        # テスト前の確認
        if not os.path.exists(self.SAMPLE_DNG):
            pytest.skip("テスト用のサンプルDNGファイルが見つかりません")
        
        # 異なるデバイス設定でのテスト
        iphone_quality = determine_optimal_quality(self.SAMPLE_DNG, 'iphone')
        ipad_quality = determine_optimal_quality(self.SAMPLE_DNG, 'ipad')
        display_quality = determine_optimal_quality(self.SAMPLE_DNG, 'display')
        
        # デバイスの特性に応じた品質関係のテスト
        assert 65 <= iphone_quality <= 90, "iPhone用の品質設定が想定範囲外です"
        assert 70 <= ipad_quality <= 90, "iPad用の品質設定が想定範囲外です"
        assert 75 <= display_quality <= 95, "ディスプレイ用の品質設定が想定範囲外です"
        
        # デバイスごとの相対的な品質関係のテスト
        assert iphone_quality <= ipad_quality <= display_quality, "デバイスごとの品質関係が想定と異なります"