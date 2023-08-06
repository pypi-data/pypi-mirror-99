from .sacred import SacredTrainer
from .base import _is_adam, default_intervals

from chainer.training import extensions

def observe_alpha(trainer):
	model = trainer.updater.get_optimizer("main").target.model
	return float(model.pool.alpha.array)

class AlphaPoolingTrainer(SacredTrainer):

	@property
	def model(self):
		return self.updater.get_optimizer("main").target.model

	def __init__(self, opts, updater, *args, **kwargs):
		super(AlphaPoolingTrainer, self).__init__(opts=opts, updater=updater, *args, **kwargs)
		### Alternating training of CNN and FC layers (only for alpha-pooling) ###
		if opts.switch_epochs:
			self.extend(SwitchTrainables(
				opts.switch_epochs,
				model=self.model,
				pooling=self.model.pool))

	def reportables(self, opts):
		print_values, plot_values = super(AlphaPoolingTrainer, self).reportables()
		alpha_update_rule = self.model.pool.alpha.update_rule
		if _is_adam(opts):
			# in case of Adam optimizer
			alpha_update_rule.hyperparam.alpha *= opts.kappa
		else:
			alpha_update_rule.hyperparam.lr *= opts.kappa

		self.extend(
			extensions.observe_value("alpha", observe_alpha),
			trigger=default_intervals.print)

		print_values.append("alpha")
		plot_values["alpha"]= ["alpha"]

		return print_values, plot_values
