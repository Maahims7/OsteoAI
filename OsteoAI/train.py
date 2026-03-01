import os
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

# configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAIN_DIR = os.path.join(BASE_DIR, 'dataset', 'train')
VAL_DIR = os.path.join(BASE_DIR, 'dataset', 'val')
TEST_DIR = os.path.join(BASE_DIR, 'dataset', 'test')
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'best_model.h5')
BATCH_SIZE = 16
IMG_SIZE = (224, 224)
EPOCHS = 15
LR = 1e-4


def create_generators():
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    val_test_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )

    val_generator = val_test_datagen.flow_from_directory(
        VAL_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )

    test_generator = val_test_datagen.flow_from_directory(
        TEST_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )

    return train_generator, val_generator, test_generator


def build_model(num_classes=3):
    base = MobileNetV2(weights='imagenet', include_top=False, input_shape=(*IMG_SIZE, 3))
    base.trainable = False

    x = base.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.5)(x)
    output = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs=base.input, outputs=output)
    model.compile(
        optimizer=Adam(learning_rate=LR),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model


def plot_history(history, out_dir=BASE_DIR):
    acc = history.history['accuracy']
    val_acc = history.history.get('val_accuracy')
    loss = history.history['loss']
    val_loss = history.history.get('val_loss')

    epochs_range = range(len(acc))

    plt.figure()
    plt.plot(epochs_range, acc, label='Train Accuracy')
    if val_acc:
        plt.plot(epochs_range, val_acc, label='Val Accuracy')
    plt.legend()
    plt.savefig(os.path.join(out_dir, 'accuracy_curve.png'))

    plt.figure()
    plt.plot(epochs_range, loss, label='Train Loss')
    if val_loss:
        plt.plot(epochs_range, val_loss, label='Val Loss')
    plt.legend()
    plt.savefig(os.path.join(out_dir, 'loss_curve.png'))


def evaluate_model(model, test_generator):
    print('Evaluating on test set...')
    results = model.evaluate(test_generator)
    print('Test loss, Test acc:', results)

    # compute confusion matrix and classification report
    from sklearn.metrics import confusion_matrix, classification_report
    y_pred = model.predict(test_generator)
    y_pred_classes = np.argmax(y_pred, axis=1)
    y_true = test_generator.classes
    cm = confusion_matrix(y_true, y_pred_classes)
    print('Confusion Matrix:\n', cm)
    print('Classification Report:\n', classification_report(y_true, y_pred_classes, target_names=list(test_generator.class_indices.keys())))

    np.save(os.path.join(BASE_DIR, 'confusion_matrix.npy'), cm)


def main():
    train_gen, val_gen, test_gen = create_generators()
    model = build_model(num_classes=len(train_gen.class_indices))

    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        MODEL_PATH,
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    )
    early = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=EPOCHS,
        callbacks=[checkpoint, early]
    )

    plot_history(history)
    evaluate_model(model, test_gen)


if __name__ == '__main__':
    main()
