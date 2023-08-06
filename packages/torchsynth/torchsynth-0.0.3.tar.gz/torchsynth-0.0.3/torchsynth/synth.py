from typing import Any, Dict, List, Optional, Tuple

import torch
import torchcsprng as csprng
from pytorch_lightning.core.lightning import LightningModule
from torch import tensor as T

from torchsynth.globals import SynthGlobals
from torchsynth.module import (
    ADSR,
    LFO,
    VCA,
    AudioMixer,
    ModulationMixer,
    MonophonicKeyboard,
    Noise,
    SineVCO,
    SquareSawVCO,
    SynthModule,
)
from torchsynth.parameter import ModuleParameter
from torchsynth.signal import Signal

# https://github.com/turian/torchsynth/issues/131
# Lightning already handles this for us
# torch.use_deterministic_algorithms(True)


class AbstractSynth(LightningModule):
    """
    Base class for synthesizers that combine one or more SynthModules
    to create a full synth architecture.

    Args:
        sample_rate (int): sample rate to run this synth at
        buffer_size (int): number of samples expected at output of child modules
    """

    def __init__(self, synthglobals: SynthGlobals, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.synthglobals = synthglobals

    @property
    def batch_size(self) -> T:
        assert self.synthglobals.batch_size.ndim == 0
        return self.synthglobals.batch_size

    @property
    def sample_rate(self) -> T:
        assert self.synthglobals.sample_rate.ndim == 0
        return self.synthglobals.sample_rate

    @property
    def buffer_size(self) -> T:
        assert self.synthglobals.buffer_size.ndim == 0
        return self.synthglobals.buffer_size

    def add_synth_modules(self, modules: List[Tuple[str, SynthModule]]):
        """
        Add a set of named children TorchSynthModules to this synth. Registers them
        with the torch nn.Module so that all parameters are recognized.

        Args:
            modules List[Tuple[str, SynthModule]]: A list of SynthModules and
                                            their names.
        """

        for name, module in modules:
            if not isinstance(module, SynthModule):
                raise TypeError(f"{module} is not a SynthModule")

            if module.batch_size != self.batch_size:
                raise ValueError(f"{module} batch_size does not match")

            if module.sample_rate != self.sample_rate:
                raise ValueError(f"{module} sample rate does not match")

            if module.buffer_size != self.buffer_size:
                raise ValueError(f"{module} buffer size does not match")

            self.add_module(name, module)

    def get_parameters(
        self, include_frozen: bool = False
    ) -> Dict[Tuple[str, str], ModuleParameter]:
        """
        Returns a dictionary of ModuleParameters for this synth keyed
        on a tuple of the SynthModule name and the parameter name
        """
        parameters = []

        # Each parameter in this synth will have a unique combination of module name
        # and parameter name -- create a dictionary keyed on that.
        for module_name, module in self.named_modules():
            # Make sure this is a SynthModule, b/c we are using ParameterDict
            # and ParameterDict is a module, we get those returned as well
            # TODO: see https://github.com/turian/torchsynth/issues/213
            if isinstance(module, SynthModule):
                for parameter in module.parameters():
                    if include_frozen or not ModuleParameter.is_parameter_frozen(
                        parameter
                    ):
                        parameters.append(
                            ((module_name, parameter.parameter_name), parameter)
                        )

        return dict(parameters)

    def set_parameters(self, params: Dict[Tuple, T], freeze: Optional[bool] = False):
        """
        Set parameters for synth by passing in a dictionary of modules and parameters.
        Can optionally freeze a parameter at this value to prevent further updates.
        """
        for (module_name, param_name), value in params.items():
            module = getattr(self, module_name)
            module.set_parameter(param_name, value.to(self.device))
            # Freeze this parameter at this value now if freeze is True
            if freeze:
                module.get_parameter(param_name).frozen = True

    def set_frozen_parameters(self, params: Dict[Tuple, float]):
        """
        Sets specific parameters within this Synth. All params within the batch
        will be set to the same value and frozen to prevent further updates.
        """
        params = {
            key: T([value] * self.batch_size, device=self.device)
            for key, value in params.items()
        }
        self.set_parameters(params, freeze=True)

    def freeze_parameters(self, params: List[Tuple]):
        """
        Freeze a set of parameters by passing in a tuple of the module and param name
        """
        for module_name, param_name in params:
            module = getattr(self, module_name)
            module.get_parameter(param_name).frozen = True

    def unfreeze_all_parameters(self):
        """
        Unfreeze all parameters in this synth
        """
        for param in self.parameters():
            if isinstance(param, ModuleParameter):
                param.frozen = False

    def _forward(self, *args: Any, **kwargs: Any) -> Signal:  # pragma: no cover
        """
        Each AbstractSynth should override this.
        """
        raise NotImplementedError("Derived classes must override this method")

    def forward(
        self, batch_idx: Optional[int] = None, *args: Any, **kwargs: Any
    ) -> Signal:  # pragma: no cover
        """
        Each AbstractSynth should override this.

        Args:
            batch_idx (Optional[int])   - If provided, we set the parameters of this
                                    synth for reproducibility, in a deterministic
                                    random way. If None (default), we just use
                                    the current module parameter settings.
        """
        if batch_idx:
            self.randomize(seed=batch_idx)
        return self._forward(*args, **kwargs)

    def test_step(self, batch, batch_idx):
        """
        This is boilerplate for lightning -- this is required by lightning Trainer
        when calling test, which we use to forward Synths on multi-gpu platforms
        """
        return T(0.0, device=self.device)

    @property
    def hyperparameters(self) -> Dict[Tuple[str, str, str], Any]:
        """
        Returns a dictionary of curve and symmetry hyperparameter values keyed
        on a tuple of the module name, parameter name, and hyperparameter name
        """
        hparams = []
        for (module_name, parameter_name), parameter in self.get_parameters().items():
            hparams.append(
                (
                    (module_name, parameter_name, "curve"),
                    parameter.parameter_range.curve,
                )
            )
            hparams.append(
                (
                    (module_name, parameter_name, "symmetric"),
                    parameter.parameter_range.symmetric,
                )
            )

        return dict(hparams)

    def set_hyperparameter(self, hyperparameter: Tuple[str, str, str], value: Any):
        """
        Set a hyperparameter. Pass in the module name, parameter name, and
        hyperparameter to set, and the value to set it to.
        """
        module = getattr(self, hyperparameter[0])
        parameter = module.get_parameter(hyperparameter[1])
        assert not ModuleParameter.is_parameter_frozen(parameter)
        setattr(parameter.parameter_range, hyperparameter[2], value)

    def randomize(self, seed: Optional[int] = None):
        """
        Randomize all parameters
        """
        if seed is not None:
            # Profile to make sure this isn't too slow?
            mt19937_gen = csprng.create_mt19937_generator(seed)
            for parameter in self.parameters():
                if not ModuleParameter.is_parameter_frozen(parameter):
                    parameter.data.uniform_(0, 1, generator=mt19937_gen)
        else:
            for parameter in self.parameters():
                if not ModuleParameter.is_parameter_frozen(parameter):
                    parameter.data = torch.rand_like(parameter, device=self.device)

        # Add seed to all modules
        for module in self._modules:
            self._modules[module].seed = seed


class Voice(AbstractSynth):
    """
    In a synthesizer, one combination of VCO, VCA, VCF's is typically called a voice.
    """

    def __init__(self, synthglobals: SynthGlobals, *args, **kwargs):
        AbstractSynth.__init__(self, synthglobals=synthglobals, *args, **kwargs)

        # Register all modules as children
        self.add_synth_modules(
            [
                ("keyboard", MonophonicKeyboard(synthglobals)),
                ("adsr_1", ADSR(synthglobals)),
                ("adsr_2", ADSR(synthglobals)),
                ("lfo_1", LFO(synthglobals)),
                ("lfo_2", LFO(synthglobals)),
                ("lfo_1_amp_adsr", ADSR(synthglobals)),
                ("lfo_2_amp_adsr", ADSR(synthglobals)),
                ("lfo_1_rate_adsr", ADSR(synthglobals)),
                ("lfo_2_rate_adsr", ADSR(synthglobals)),
                ("mod_matrix", ModulationMixer(synthglobals, n_input=4, n_output=5)),
                ("vco_1", SineVCO(synthglobals)),
                ("vco_2", SquareSawVCO(synthglobals)),
                ("noise", Noise(synthglobals)),
                ("vca", VCA(synthglobals)),
                ("mixer", AudioMixer(synthglobals, n_input=3, curves=[1.0, 1.0, 0.1])),
            ]
        )

    def _forward(self) -> T:
        # The convention for triggering a note event is that it has
        # the same note_on_duration for both ADSRs.
        midi_f0, note_on_duration = self.keyboard()

        # ADSRs for modulating LFOs
        lfo_1_rate = self.lfo_1_rate_adsr(note_on_duration)
        lfo_2_rate = self.lfo_2_rate_adsr(note_on_duration)
        lfo_1_amp = self.lfo_1_amp_adsr(note_on_duration)
        lfo_2_amp = self.lfo_2_amp_adsr(note_on_duration)

        # Compute LFOs with envelopes
        lfo_1 = self.vca(self.lfo_1(lfo_1_rate), lfo_1_amp)
        lfo_2 = self.vca(self.lfo_2(lfo_2_rate), lfo_2_amp)

        # ADSRs for Oscillators and noise
        adsr_1 = self.adsr_1(note_on_duration)
        adsr_2 = self.adsr_2(note_on_duration)

        # Mix all modulation signals
        modulation = self.mod_matrix(adsr_1, adsr_2, lfo_1, lfo_2)

        # Create signal and with modulations and mix together
        vco_1_out = self.vca(self.vco_1(midi_f0, modulation[0]), modulation[1])
        vco_2_out = self.vca(self.vco_2(midi_f0, modulation[2]), modulation[3])
        noise_out = self.vca(self.noise(device=self.device), modulation[4])

        return self.mixer(vco_1_out, vco_2_out, noise_out)
