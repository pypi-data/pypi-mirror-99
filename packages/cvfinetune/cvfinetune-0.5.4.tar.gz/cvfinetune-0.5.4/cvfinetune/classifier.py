import abc
import chainer
import chainer.functions as F
import chainer.links as L
import logging

from chainer_addons.models.classifier import Classifier as C

class Classifier(C):

	def __init__(self, *args, **kwargs):
		super(Classifier, self).__init__(*args, **kwargs)

		assert hasattr(self, "model"), \
			"This classifiert has no \"model\" attribute!"

	@property
	def feat_size(self):
		if hasattr(self.model.pool, "output_dim") and self.model.pool.output_dim is not None:
			return self.model.pool.output_dim

		return self.model.meta.feature_size

	@property
	def output_size(self):
		return self.feat_size

	def enable_only_head(self):
		self.model.disable_update()
		self.model.fc.enable_update()


class SeparateModelClassifier(Classifier):
	"""Classifier, that holds two separate models"""

	def __init__(self, *args, **kwargs):
		super(SeparateModelClassifier, self).__init__(*args, **kwargs)

		with self.init_scope():
			self.init_separate_model()

	@abc.abstractmethod
	def __call__(self, *args, **kwargs):
		super(SeparateModelClassifier, self).__call__(*args, **kwargs)

	def init_separate_model(self):

		if hasattr(self, "separate_model"):
			logging.warn("Global Model already initialized! Skipping further execution!")
			return

		self.separate_model = self.model.copy(mode="copy")

	def loader(self, model_loader):

		def inner(n_classes, feat_size):
			# use the given feature size here
			model_loader(n_classes=n_classes, feat_size=feat_size)

			# use the given feature size first ...
			self.separate_model.reinitialize_clf(
				n_classes=n_classes,
				feat_size=feat_size)

			# then copy model params ...
			self.separate_model.copyparams(self.model)

			# now use the default feature size to re-init the classifier
			self.separate_model.reinitialize_clf(
				n_classes=n_classes,
				feat_size=self.feat_size)

		return inner

	def enable_only_head(self):
		super(SeparateModelClassifier, self).enable_only_head()
		self.separate_model.disable_update()
		self.separate_model.fc.enable_update()
