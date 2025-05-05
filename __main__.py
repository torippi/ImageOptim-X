#!/usr/bin/env python3
"""
ImageOptim-X のメインスクリプト
このファイルにより、パッケージを直接実行できるようになります
例: python -m imageoptim_x
"""

import sys
import argparse
from tqdm import tqdm
import os

from imageoptim_x.core.converter import convert_raw_to_jpeg
from imageoptim_x.core.optimizer import determine_optimal_quality
from imageoptim_x.core.metadata import extract_raw_metadata, apply_metadata_to_jpeg
from imageoptim_x.utils.file_utils import ensure_directory_exists, find_raw_files, get_output_path

def main():
    """メイン実行関数"""
    # コマンドライン引数の設定
    parser = argparse.ArgumentParser(description='ImageOptim-X: iPhone ProRAW DNG最適化ツール')
    parser.add_argument('source_dir', help='RAWファイルが格納されているディレクトリのパス')
    parser.add_argument('output_dir', help='変換後のJPEGを保存するディレクトリのパス')
    parser.add_argument('--quality', type=int, default=0, help='JPEG変換時の品質（0-100）。0の場合は自動決定。')
    parser.add_argument('--device', choices=['iphone', 'ipad', 'display'], help='出力の対象デバイス')
    parser.add_argument('--preserve-metadata', action='store_true', help='メタデータを保持する')
    
    args = parser.parse_args()
    
    # 出力ディレクトリの確認/作成
    ensure_directory_exists(args.output_dir)
    
    # RAWファイルの検索
    raw_files = find_raw_files(args.source_dir)
    
    if not raw_files:
        print(f"エラー: {args.source_dir} にRAWファイルが見つかりませんでした。")
        sys.exit(1)
    
    print(f"{len(raw_files)}個のRAWファイルが見つかりました。処理を開始します...")
    
    # 処理結果の統計
    total_original_size = 0
    total_output_size = 0
    successful_conversions = 0
    
    # ファイル処理ループ
    for raw_file in tqdm(raw_files, desc="変換中"):
        try:
            # 出力パスの取得
            output_path = get_output_path(raw_file, args.output_dir)
            
            # 品質設定
            quality = args.quality
            if quality == 0:  # 自動決定
                quality = determine_optimal_quality(raw_file, args.device)
            
            # RAWファイルの変換
            result = convert_raw_to_jpeg(raw_file, output_path, quality)
            
            # メタデータの処理
            if args.preserve_metadata:
                metadata = extract_raw_metadata(raw_file)
                apply_metadata_to_jpeg(output_path, metadata)
            
            # 統計の更新
            total_original_size += result['original_size']
            total_output_size += result['output_size']
            successful_conversions += 1
            
        except Exception as e:
            print(f"エラー: {os.path.basename(raw_file)} の処理中に問題が発生しました - {str(e)}")
    
    # 結果レポート
    if successful_conversions > 0:
        reduction_rate = (1 - total_output_size/total_original_size) * 100
        
        print("\n===== 処理完了 =====")
        print(f"処理ファイル数: {successful_conversions}/{len(raw_files)}")
        print(f"元のサイズ合計: {total_original_size/(1024*1024):.2f}MB")
        print(f"変換後のサイズ合計: {total_output_size/(1024*1024):.2f}MB")
        print(f"総削減率: {reduction_rate:.2f}%")
        print(f"ファイルは {args.output_dir} に保存されました。")
    else:
        print("エラー: すべてのファイルの処理に失敗しました。")

if __name__ == "__main__":
    main()