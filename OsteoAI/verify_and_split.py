#!/usr/bin/env python3
"""
Verify current dataset split and optionally resplit with 70/15/15 ratio
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict
from sklearn.model_selection import train_test_split

def count_images(dataset_root):
    """Count images in each split and class"""
    stats = defaultdict(lambda: defaultdict(int))
    total = 0
    
    for split in ['train', 'val', 'test']:
        for cls in ['Normal', 'Osteopenia', 'Osteoporosis']:
            path = os.path.join(dataset_root, split, cls)
            if os.path.exists(path):
                count = len([f for f in os.listdir(path) 
                           if os.path.isfile(os.path.join(path, f)) 
                           and f.lower().endswith(('.jpg', '.jpeg', '.png'))])
                stats[split][cls] = count
                total += count
    
    return stats, total

def print_statistics(stats, total):
    """Print dataset statistics"""
    print("\n" + "="*70)
    print("DATASET SPLIT STATISTICS")
    print("="*70)
    
    for split in ['train', 'val', 'test']:
        split_total = sum(stats[split].values())
        pct = (split_total / total * 100) if total > 0 else 0
        print(f"\n{split.upper()} ({pct:.1f}%):")
        print(f"  Total: {split_total}")
        for cls in ['Normal', 'Osteopenia', 'Osteoporosis']:
            count = stats[split][cls]
            print(f"    {cls:15s}: {count:4d}")
    
    print(f"\nTOTAL IMAGES: {total}")
    print("="*70 + "\n")

def resplit_dataset(src_root, dst_root='dataset', train_frac=0.7, val_frac=0.15, test_frac=0.15, seed=42):
    """Resplit dataset with exact 70/15/15 ratio"""
    print("\nReorganizing dataset with 70/15/15 split...")
    
    # Prepare destination directories
    for split in ['train', 'val', 'test']:
        for cls in ['Normal', 'Osteopenia', 'Osteoporosis']:
            os.makedirs(os.path.join(dst_root, split, cls), exist_ok=True)
    
    # Collect all images by class
    for cls in ['Normal', 'Osteopenia', 'Osteoporosis']:
        all_images = []
        
        # Gather images from all current splits
        for split in ['train', 'val', 'test']:
            src_cls_dir = os.path.join(src_root, split, cls)
            if os.path.exists(src_cls_dir):
                for f in os.listdir(src_cls_dir):
                    if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                        all_images.append(os.path.join(src_cls_dir, f))
        
        if not all_images:
            print(f"  ⚠️  No images found for class '{cls}'")
            continue
        
        # Split: 70% train, 15% val, 15% test
        train_val, test_set = train_test_split(
            all_images, test_size=test_frac, random_state=seed
        )
        val_relative = val_frac / (train_frac + val_frac)
        train_set, val_set = train_test_split(
            train_val, test_size=val_relative, random_state=seed
        )
        
        # Copy to destination
        for fpath in train_set:
            shutil.copy2(fpath, os.path.join(dst_root, 'train', cls, os.path.basename(fpath)))
        
        for fpath in val_set:
            shutil.copy2(fpath, os.path.join(dst_root, 'val', cls, os.path.basename(fpath)))
        
        for fpath in test_set:
            shutil.copy2(fpath, os.path.join(dst_root, 'test', cls, os.path.basename(fpath)))
        
        print(f"  ✓ {cls:15s}: {len(train_set)} train, {len(val_set)} val, {len(test_set)} test")
    
    print("\n✅ Dataset resplit complete!\n")

if __name__ == '__main__':
    import sys
    
    dataset_root = 'dataset'
    
    # Show current statistics
    print("\n📊 CHECKING CURRENT DATASET SPLIT...")
    stats, total = count_images(dataset_root)
    print_statistics(stats, total)
    
    # Verify if split is 70/15/15
    train_pct = (sum(stats['train'].values()) / total * 100) if total > 0 else 0
    val_pct = (sum(stats['val'].values()) / total * 100) if total > 0 else 0
    test_pct = (sum(stats['test'].values()) / total * 100) if total > 0 else 0
    
    print(f"📈 Current Ratio: Train={train_pct:.1f}%, Val={val_pct:.1f}%, Test={test_pct:.1f}%")
    
    if abs(train_pct - 70) < 0.5 and abs(val_pct - 15) < 0.5 and abs(test_pct - 15) < 0.5:
        print("✅ Dataset is already split at 70/15/15 ratio!")
    else:
        print("\n⚠️  Dataset ratio differs from 70/15/15")
        response = input("Do you want to resplit the dataset? (y/n): ").strip().lower()
        if response == 'y':
            resplit_dataset(dataset_root)
            stats, total = count_images(dataset_root)
            print_statistics(stats, total)
