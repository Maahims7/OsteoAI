import os
import shutil
from sklearn.model_selection import train_test_split


def prepare_dirs(root, classes):
    for phase in ['train', 'val', 'test']:
        for cls in classes:
            d = os.path.join(root, phase, cls)
            os.makedirs(d, exist_ok=True)


def split_dataset(src_root, dst_root, train_frac=0.7, val_frac=0.15, test_frac=0.15, seed=42):
    """Split images located in src_root/<class> into train/val/test subfolders under dst_root."""
    assert abs(train_frac + val_frac + test_frac - 1.0) < 1e-6, 'Fractions must sum to 1'

    classes = [d for d in os.listdir(src_root) if os.path.isdir(os.path.join(src_root, d))]
    if not classes:
        raise RuntimeError(f'No class subdirectories found in {src_root}')

    prepare_dirs(dst_root, classes)

    for cls in classes:
        src_cls_dir = os.path.join(src_root, cls)
        images = [os.path.join(src_cls_dir, f) for f in os.listdir(src_cls_dir)
                  if os.path.isfile(os.path.join(src_cls_dir, f))]
        if not images:
            continue

        train_and_val, test = train_test_split(images, test_size=test_frac, random_state=seed)
        # adjust val fraction relative to remaining
        val_relative = val_frac / (train_frac + val_frac)
        train, val = train_test_split(train_and_val, test_size=val_relative, random_state=seed)

        for lst, phase in [(train, 'train'), (val, 'val'), (test, 'test')]:
            dest_dir = os.path.join(dst_root, phase, cls)
            for path in lst:
                fname = os.path.basename(path)
                shutil.copy2(path, os.path.join(dest_dir, fname))
        print(f'class {cls}: {len(train)} train, {len(val)} val, {len(test)} test samples')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Split dataset into train/val/test')
    parser.add_argument('src', help='Source root directory containing class subfolders')
    parser.add_argument('--dst', default='dataset', help='Destination root for split folders')
    parser.add_argument('--train', type=float, default=0.7)
    parser.add_argument('--val', type=float, default=0.15)
    parser.add_argument('--test', type=float, default=0.15)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()

    split_dataset(args.src, args.dst, args.train, args.val, args.test, seed=args.seed)
