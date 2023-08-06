"""Generic Wrapper for Transformer-Based models."""

import pandas as pd
from simpletransformers.classification import ClassificationModel
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.preprocessing import LabelEncoder


class SimpletransformersBertModel(BaseEstimator, ClassifierMixin):
    """Generic Wrapper for Transformer Models."""

    def __init__(
            self,
            model_type='distilbert',
            pretrained_model='distilbert-base-uncased',
            output_dir='outputs/',
            cache_dir='cache/',
            fp16=False,
            fp16_opt_level='O1',
            max_seq_length=256,
            train_batch_size=8,
            eval_batch_size=8,
            gradient_accumulation_steps=1,
            num_train_epochs=1,
            weight_decay=0,
            learning_rate=4e-5,
            adam_epsilon=1e-8,
            warmup_ratio=0.06,
            warmup_steps=0,
            max_grad_norm=1.0,
            logging_steps=0,
            evaluate_during_training=False,
            save_steps=-1,
            save_eval_checkpoints=False,
            save_model_every_epoch=False,
            no_cache=False,
            no_save=False,
            eval_all_checkpoints=True,
            use_tensorboard=False,
            overwrite_output_dir=False,
            reprocess_input_data=True,
            use_gpu=False,
            use_cuda=False,
            n_gpu=1,
            silent=False,
            use_multiprocessing=True,
            sliding_window=True,
    ):
        """Look at the documentation of simpletransformers for details."""
        self.model_type = model_type
        self.pretrained_model = pretrained_model
        self.output_dir = output_dir
        self.cache_dir = cache_dir
        self.fp16 = fp16
        self.fp16_opt_level = fp16_opt_level
        self.max_seq_length = max_seq_length
        self.train_batch_size = train_batch_size
        self.eval_batch_size = eval_batch_size
        self.gradient_accumulation_steps = gradient_accumulation_steps
        self.num_train_epochs = num_train_epochs
        self.weight_decay = weight_decay
        self.learning_rate = learning_rate
        self.adam_epsilon = adam_epsilon
        self.warmup_ratio = warmup_ratio
        self.warmup_steps = warmup_steps
        self.max_grad_norm = max_grad_norm
        self.logging_steps = logging_steps
        self.evaluate_during_training = evaluate_during_training
        self.save_steps = save_steps
        self.eval_all_checkpoints = eval_all_checkpoints
        self.use_tensorboard = use_tensorboard
        self.overwrite_output_dir = overwrite_output_dir
        self.reprocess_input_data = reprocess_input_data
        self.use_cuda = use_cuda
        self.silent = silent
        self.use_multiprocessing = use_multiprocessing
        self.sliding_window = sliding_window
        self.save_eval_checkpoints = save_eval_checkpoints
        self.save_model_every_epoch = save_model_every_epoch
        self.no_cache = no_cache
        self.no_save = no_save

    def fit(self, x, y, *args, **kwargs):
        """Fit the model."""
        self.label_encoder = LabelEncoder()
        y = self.label_encoder.fit_transform(y)
        targets = set(y)
        n_classes = len(targets)

        for target in targets:
            if target >= n_classes:
                raise Exception(
                    f'target {target} is larger than n_classes ({n_classes}). '
                    'this is not supported by pytorch and will cause a very '
                    'hard to debug error.'
                )

        model_args = {
            'model_type': self.model_type,
            'pretrained_model': self.pretrained_model,
            'output_dir': self.output_dir,
            'cache_dir': self.cache_dir,
            'fp16': self.fp16,
            'fp16_opt_level': self.fp16_opt_level,
            'max_seq_length': self.max_seq_length,
            'train_batch_size': self.train_batch_size,
            'eval_batch_size': self.eval_batch_size,
            'gradient_accumulation_steps': self.gradient_accumulation_steps,
            'num_train_epochs': self.num_train_epochs,
            'weight_decay': self.weight_decay,
            'learning_rate': self.learning_rate,
            'adam_epsilon': self.adam_epsilon,
            'warmup_ratio': self.warmup_ratio,
            'warmup_steps': self.warmup_steps,
            'max_grad_norm': self.max_grad_norm,
            'logging_steps': self.logging_steps,
            'evaluate_during_training': self.evaluate_during_training,
            'save_steps': self.save_steps,
            'eval_all_checkpoints': self.eval_all_checkpoints,
            'use_tensorboard': self.use_tensorboard,
            'overwrite_output_dir': self.overwrite_output_dir,
            'reprocess_input_data': self.reprocess_input_data,
            'silent': self.silent,
            'use_multiprocessing': self.use_multiprocessing,
            'dataloader_num_workers': 0,
            'sliding_window': self.sliding_window,
            'save_eval_checkpoints': self.save_eval_checkpoints,
            'save_model_every_epoch': self.save_model_every_epoch,
            'no_save': self.no_save,
            'no_cache': self.no_cache,
        }

        self.model = ClassificationModel(
            self.model_type,
            self.pretrained_model,
            num_labels=n_classes,
            args=model_args,
            use_cuda=self.use_cuda,
        )
        df = pd.DataFrame(dict(text=x, labels=y))
        self.model.train_model(df)

    def predict(self, x, *args, **kwargs):
        """Predict unseen documents."""
        result, raw = self.model.predict(x)
        result = self.label_encoder.inverse_transform(result)
        return result
