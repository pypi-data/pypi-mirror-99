from dataclasses import dataclass, field
from typing      import List, Any
from torch       import Tensor
from ase         import Atoms
from ase.io      import read

import numpy      as np
import schnetpack as spk

import torch
import os, sys, shutil
from schnetpack.atomistic.model import AtomisticModel
from schnetpack                 import AtomsLoader
from schnetpack                 import AtomsData
from schnetpack.train.metrics   import MeanAbsoluteError, RootMeanSquaredError, MeanSquaredError
from schnetpack.train           import Trainer, CSVHook, ReduceLROnPlateauHook
from schnetpack.train           import build_mse_loss
from storer                     import Storer

import warnings
warnings.filterwarnings("ignore")

from tqdm import tqdm
if tqdm: print_function = tqdm.write
else:    print_function = print

@dataclass
class NNClass:
    __version__                  : str            = "1.4.8"
    debug                        : bool           = False

    internal_name                : str            = "[NNClass]"
    system_path                  : str            = "."
    plot_enabled                 : bool           = False
    meta                         : bool           = True
    storer                       : object         = None
    device                       : str            = "cuda" if torch.cuda.is_available() else "cpu"
    network_name                 : str            = "unknower"
    info                         : dict           = field(default_factory=dict)
    #
    db_properties                : tuple          = ("energy", "forces", "dipole_moment")  # properties look for database
    training_properties          : tuple          = ("energy", "forces", "dipole_moment")  # properties used for training
    db_epochs                    : dict           = field(default_factory=dict)
    training_progress            : dict           = field(default_factory=dict)
    #
    redo_split_file              : bool           = False
    foreign_plotted              : bool           = False
    loss_tradeoff                : tuple          = (0.2, 0.8, 0.5)
    lr                           : float          = 1e-4
    predict_each_epoch           : int            = 10

    batch_size                   : int            = 16
    n_features                   : int            = 128
    n_filters                    : int            = 128
    n_gaussians                  : int            = 25
    n_interactions               : int            = 1
    cutoff                       : int            = 5.0  # angstrems

    n_layers_energy_force        : int            = 2
    n_layers_dipole_moment       : int            = 2
    n_neurons_energy_force       : int            = None
    n_neurons_dipole_moment      : int            = None

    #
    using_matplotlib             : bool           = False
    compare_with_foreign_model   : bool           = False
    visualize_each_point_from_nn : int            = 5
    visualize_points_from_data   : int            = 100
    #
    samples                      : List[Atoms]    = None
    model                        : AtomisticModel = None
    trainer                      : Trainer        = None
    train_loader                 : AtomsLoader    = None
    valid_loader                 : AtomsLoader    = None
    test_loader                  : AtomsLoader    = None

    train_samples                : np.array       = None
    valid_samples                : np.array       = None
    test_samples                 : np.array       = None

    number_training_examples_percent  : float     = 60.0
    number_validation_examples_percent: float     = 20.0

    def __post_init__(self):
        if self.system_path[-1] != "/": self.system_path+="/"
        #
        self.xyz_path              = os.path.expanduser(self.system_path) + "xyz/"
        self.db_path               = os.path.expanduser(self.system_path) + "dbs/"
        self.general_models_path   = os.path.expanduser(self.system_path) + "models/"
        self.split_path            = os.path.expanduser(self.system_path) + "splits/"
        self.test_path             = os.path.expanduser(self.system_path) + "tests/"
        self.path2foreign_model    = os.path.expanduser(self.system_path) + "foreign_model/"
        #
        os.makedirs(os.path.dirname(self.db_path),             exist_ok=True)
        os.makedirs(os.path.dirname(self.general_models_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.split_path),          exist_ok=True)
        os.makedirs(os.path.dirname(self.test_path),           exist_ok=True)

        if self.plot_enabled:
            try:
                sys.path.insert(0, os.path.expanduser("~/") + "bin")  # Plotter...
                from Plotter import Plotter
                self.using_matplotlib = False
            except:
                print_function(f"Sorry. Plotter is not available. Matplotlib will be in use...")
                import matplotlib.pyplot as plt
                self.using_matplotlib = True

        if not self.using_matplotlib and self.plot_enabled:
             self.plotter_progress = Plotter(title="Check Results", pages_info=dict(
                 xyz_file     = dict(xname="[DFT steps]", yname="Energy [Hartree]",),
                 xyz_file_sub = dict(xname="[DFT steps]", yname="Energy-(int)E[0], [Hartree]",),
                 energy_mae   = dict(xname="Time [s]"   , yname="Energy MAE [Hartree]",),
                 forces_mae   = dict(xname="Time [s]"   , yname="Forces MAE [Hartree/\u212B]",),
                 e_diff       = dict(xname="[DFT steps]", yname="\\Delta Energy [Hartree]",),
        ))

        # info
        kf = self.network_name+"_features"
        try:
            db_epochs = self.info[self.network_name]
        except KeyError:
            available_nns = []
            for k in self.info:
                if not str(k).endswith("_features"): available_nns.append(k)

            print_function(f"There is no information about [{self.network_name}] network in `info`")
            print_function(f"Known NN: {available_nns}")
            sys.exit(1)

        self.db_epochs               = self.info[self.network_name]
        self.predict_each_epoch      = self.info[kf].get("predict_each_epoch")      if self.info[kf].get("predict_each_epoch")      else self.predict_each_epoch
        self.lr                      = self.info[kf].get("lr")                      if self.info[kf].get("lr")                      else self.lr
        self.batch_size              = self.info[kf].get("batch_size")              if self.info[kf].get("batch_size")              else self.batch_size

        self.n_features              = self.info[kf].get("n_features")              if self.info[kf].get("n_features")              else self.n_features
        self.n_filters               = self.info[kf].get("n_filters")               if self.info[kf].get("n_filters")               else self.n_filters
        self.n_interactions          = self.info[kf].get("n_interactions")          if self.info[kf].get("n_interactions")          else self.n_interactions
        self.n_gaussians             = self.info[kf].get("n_gaussians")             if self.info[kf].get("n_gaussians")             else self.n_gaussians
        self.cutoff                  = self.info[kf].get("cutoff")                  if self.info[kf].get("cutoff")                  else self.cutoff

        self.db_properties           = self.info[kf].get("db_properties")           if self.info[kf].get("db_properties")           else self.db_properties
        self.training_properties     = self.info[kf].get("training_properties")     if self.info[kf].get("training_properties")     else self.training_properties
        self.loss_tradeoff           = self.info[kf].get("loss_tradeoff")           if self.info[kf].get("loss_tradeoff")           else self.loss_tradeoff

        self.n_layers_energy_force   = self.info[kf].get("n_layers_energy_force")   if self.info[kf].get("n_layers_energy_force")   else self.n_layers_energy_force
        self.n_neurons_energy_force  = self.info[kf].get("n_neurons_energy_force")  if self.info[kf].get("n_neurons_energy_force")  else self.n_neurons_energy_force

        self.n_layers_dipole_moment  = self.info[kf].get("n_layers_dipole_moment")  if self.info[kf].get("n_layers_dipole_moment")  else self.n_layers_dipole_moment
        self.n_neurons_dipole_moment = self.info[kf].get("n_neurons_dipole_moment") if self.info[kf].get("n_neurons_dipole_moment") else self.n_neurons_dipole_moment

        self.number_training_examples_percent   = self.info[kf].get("number_training_examples_percent")   if self.info[kf].get("number_training_examples_percent")   else self.number_training_examples_percent
        self.number_validation_examples_percent = self.info[kf].get("number_validation_examples_percent") if self.info[kf].get("number_validation_examples_percent") else self.number_validation_examples_percent

        self.check_provided_parameters()
        print_function(f"{self.internal_name} [v.{self.__version__}] | System path: {self.system_path}")
        if self.debug: print_function(f"<<<Debug call>>>\n {str(self)}"); sys.exit(0)


    def check_provided_parameters(self) -> None:
        ok = True; mess = ""
        # 1
        if (self.number_training_examples_percent + self.number_validation_examples_percent) >= 100:
            ok, mess = False, "Training[%] + Validation[%] have to be smaller than 100% | The rest samples are for tests purpose."
        # 2...

        if not ok: print_function(mess); sys.exit(1)

    @staticmethod
    def loss_function(batch: Any, result: Any) -> Tensor:
        # tradeoff
        rho_tradeoff = 0.1
        # compute the mean squared error on the energies
        diff_energy = batch["energy"]-result["energy"]
        err_sq_energy = torch.mean(diff_energy**2)

        # compute the mean squared error on the forces
        diff_forces = batch["forces"]-result["forces"]
        err_sq_forces = torch.mean(diff_forces**2)

        # build the combined loss function
        err_sq = rho_tradeoff*err_sq_energy + (1-rho_tradeoff)*err_sq_forces

        return err_sq

    @staticmethod
    def find_dbs(db_path: Any) -> List:
        db_list = []
        for db_file in os.listdir(db_path):
            if db_file.endswith(".db"):
                db_fname = os.fsdecode(db_file)
                print_function(f"     Found: {db_fname}")
                db_list.append(db_fname)
        return db_list

    def print_info(self) -> None:
        print_function(f"""
# # # # # # # # # # # [INFORMATION | device {self.device}:{list(range(torch.cuda.device_count()))}] # # # # # # # # # # #
        NUMBER TRAINING EXAMPLES  [%]:   {self.number_training_examples_percent}
        NUMBER VALIDATION EXAMPLES[%]:   {self.number_validation_examples_percent}
        LEARNING RATE                :   {self.lr}
        N INTERACTION                :   {self.n_interactions}
        LOSS TRADEOFF                :   {self.loss_tradeoff}
        TRAINING PROPERTIES          :   {self.training_properties}

        DB INFO:
            PROPERTIES               :   {self.db_properties}
            [INDEXES : EPOCHS]       :   {self.db_epochs.items()}

        PATHS:
            XYZ                      :   {self.xyz_path}
            DB                       :   {self.db_path}
            MODEL [GENERAL]          :   {self.general_models_path}
            SPLITS                   :   {self.split_path}

        """)
        self.storer.show()

    def create_model_path(self, redo:bool = False) -> None:
        self.model_path   = self.general_models_path + self.network_name

        if redo:
            ans = input("Are you sure with removing the trained model? [y/n]\n")
            if ans == "y":
                print_function(
                    """
                    REMOVING THE PREVIOUS MODEL (IF EXIST) + TEST_FOLDER

                    """
                )
                # before setting up the trainer, remove previous model and tests
                try: shutil.rmtree(self.model_path)
                except FileNotFoundError: pass
                try: shutil.rmtree(self.test_path + self.network_name)
                except FileNotFoundError: pass
            else:
                print_function(f"Skipping removing...")

        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        self.storer  = Storer(dump_name=self.network_name, dump_path=self.model_path, compressed=False)

    def plot_training_progress(self) -> None:
        # TODO: REFACTORING
        #
        with open(os.path.join(self.model_path, 'log.csv')) as flog: head = [next(flog) for line in range(1)]
        titles = head[0].strip().lower().split(",")
        # Load logged results
        results = np.loadtxt(os.path.join(self.model_path, 'log.csv'), skiprows=1, delimiter=',')

        self.training_progress.clear()  # clear before use
        for idx, title in enumerate(titles): self.training_progress[title] = results[:, idx]

        # Determine time axis
        time = results[:,0]-results[0,0]
        print_function(f"Time: {time}")
        time_ = self.training_progress['time'] - self.training_progress['time'][0]
        print_function(f"Time_: {time_}")

        # Load the validation MAEs
        if 'energy' in self.training_properties: energy_mae = self.training_progress['mae_energy']
        if 'forces' in self.training_properties: forces_mae = self.training_progress['mae_forces']

        # Get final validation errors
        print_function('Validation MAE:')
        print_function('    energy: {:10.5f} Hartree'.format(energy_mae[-1]))
        print_function('    forces: {:10.5f} Hartree/\u212B'.format(forces_mae[-1]))

        if not self.using_matplotlib:
            self.plotter_progress.plot(x=time, y=energy_mae, key_name="", page="energy_mae")
            self.plotter_progress.plot(x=time, y=forces_mae, key_name="", page="forces_mae")
        else:
            # Matplotlib instructions
            plt.figure(figsize=(14,5))

            # Plot energies
            plt.subplot(1,2,1)
            plt.plot(time, energy_mae)
            plt.title('Energy')
            plt.ylabel('MAE [Hartree]')
            plt.xlabel('Time [s]')

            # Plot forces
            plt.subplot(1,2,2)
            plt.plot(time, forces_mae)
            plt.title('Forces')
            plt.ylabel('MAE [Hartree/\u212B]')
            plt.xlabel('Time [s]')
            plt.show()

    def prepare_databases(self, redo:bool = False, index:str = "0:10:10", xyz_file:str = "noname.xyz") -> None:
        # recreating databases
        if redo:
            db_list = NNClass.find_dbs(db_path=self.db_path)
            print_function(f"{self.internal_name} [Re-creating databases...]")
            for db_fname in db_list:
                os.remove(self.db_path + db_fname)
                print_function(f"     {db_fname} removed.")

        print_function(f"{self.internal_name} Checking databases...")
        db_path_fname = os.path.join(self.db_path, xyz_file + "_"+ str(index) + ".db")
        if os.path.exists(db_path_fname): print_function(f" - - -> {index} [OK]")
        else:
            # no databases is found
            print_function(f"{self.internal_name} Preparing databases...")
            print_function(f"Creating db with indexes: {index}")
            property_list = []
            samples = read(self.xyz_path + xyz_file, index=index, format="extxyz")
            for sample in tqdm(samples):
                # All properties need to be stored as numpy arrays
                # Note: The shape for scalars should be (1,), not ()
                # Note: GPUs work best with float32 data
                # Note: BE SURE if results are not suffer from lack of precision.
                _ = dict()
                if 'energy' in self.db_properties:
                    try:
                        energy = np.array([sample.info['energy']], dtype=np.float32); _['energy'] = energy
                    except Exception as e: print_function(f"[Warning]: {e}")
                if 'forces' in self.db_properties:
                    try:
                        forces = np.array(sample.get_forces(),   dtype=np.float32); _['forces'] = forces
                    except Exception as e: print_function(f"[Warning]: {e}")
                if 'dipole_moment' in self.db_properties:
                    try:
                        dipole_moment = np.array(sample.get_dipole_moment(), dtype=np.float32); _['dipole_moment'] = dipole_moment
                    except Exception as e: print_function(f"[Warning]: {e}")
                property_list.append(_)

            # Creating DB
            new_dataset = AtomsData(db_path_fname, available_properties=self.db_properties)
            new_dataset.add_systems(samples, property_list)

            print_function(f"Creating databases for {self.xyz_path} is done!")

    def prepare_train_valid_test_samples(self, db_name:str = "xyzname.xyz_indexes.db") -> None:
        print_function(f"{self.internal_name} Preparing train/valid/test samples...")

        # loading db
        db_path_fname = self.db_path + db_name
        print_function(f"Loading... | {db_path_fname}")
        self.samples = AtomsData(db_path_fname, load_only=self.training_properties)  # pick the db

        # take first atoms/props
        atoms, props = self.samples.get_properties(idx=0)
        print_function(f"->>> 1 sample[{atoms.symbols}]")
        print('->>> [DB] Properties:\n', *[' -- {:s}\n'.format(key) for key in props.keys()])

        number_training_examples   = int(len(self.samples) * (self.number_training_examples_percent   / 100))
        number_validation_examples = int(len(self.samples) * (self.number_validation_examples_percent / 100))

        # creating path_file
        self.split_path_file = os.path.join(self.split_path, f"{db_name}_split_Ntrain{number_training_examples}_Nvalid{number_validation_examples}_{self.network_name}.npz")

        # removing if redo
        if self.redo_split_file:
            print_function(f"{self.internal_name} [Recreating split.npz]")
            try: os.remove(self.split_path_file)
            except FileNotFoundError: pass

        # split train validation testf
        self.train_samples, self.valid_samples, self.test_samples = spk.train_test_split(
            data       = self.samples,
            num_train  = number_training_examples,
            num_val    = number_validation_examples,
            split_file = self.split_path_file,  # WARNING! if the file exists it will be loaded.
        )

        print_function(f"{self.internal_name} Creating train/validation/test loader...")
        # PIN MEMORY <-?-> Savage of memory?
        self.train_loader = AtomsLoader(self.train_samples, batch_size=self.batch_size, num_workers=4, pin_memory=False, shuffle=True,)
        self.valid_loader = AtomsLoader(self.valid_samples, batch_size=self.batch_size, num_workers=4, pin_memory=False)
        self.test_loader  = AtomsLoader(self.test_samples,  batch_size=self.batch_size, num_workers=4, pin_memory=False)

        print_function(f"{self.internal_name} [train/valid/test] done.")

    def build_model(self) -> None:
        print_function(f"{self.internal_name} Checking the model...")
        if os.path.exists(self.model_path + "/best_model"):
            print_function(f"{self.internal_name} Already trained network exists!")
            print_function(f"Loading...")
            self.model = torch.load(self.model_path + "/best_model")
            print_function(f"Model parameters: {self.model}")

        else:
            print_function(f"[WARNING] No neural network!")
            print_function(f"{self.internal_name} Building the model...")
            output_modules = []

            representation = spk.SchNet(
                n_atom_basis         = self.n_features,
                n_filters            = self.n_filters,
                n_interactions       = self.n_interactions,
                cutoff               = self.cutoff,
                n_gaussians          = self.n_gaussians,    # 25    -- default
                normalize_filter     = False,               # False -- default
                coupled_interactions = False,               # False -- default
                return_intermediate  = False,               # False -- default
                max_z                = 100,                 # 100   -- default
                charged_systems      = False,               # False -- default
                cutoff_network       = spk.nn.cutoff.CosineCutoff,
                )

            if "energy" in self.training_properties or "forces" in self.training_properties:

                per_atom = dict(energy=True, forces=False, dipole_moment=False)
                try:
                    means, stddevs = self.train_loader.get_statistics(property_names  = list(self.training_properties),
                                                                  divide_by_atoms = per_atom,
                                                                  single_atom_ref = None)
                    print_function('Mean atomization energy      / atom: {:12.4f} [Hartree]'.format(means  ["energy"][0]))
                    print_function('Std. dev. atomization energy / atom: {:12.4f} [Hartree]'.format(stddevs["energy"][0]))
                    means_energy  = means  ["energy"]
                    stddevs_enegy = stddevs["energy"]
                except:
                    # Not consistent data
                    print("[NOTE] Provided samples are not consistent!")
                    means_energy  = None
                    stddevs_enegy = None

                ENERGY_FORCE = spk.atomistic.Atomwise(
                    n_in             = representation.n_atom_basis,
                    n_out            = 1,                            # 1    -- default
                    aggregation_mode = "sum",                        # sum  -- default
                    n_layers         = self.n_layers_energy_force,   # 2    -- default
                    n_neurons        = self.n_neurons_energy_force,  # None -- default
                    property         = "energy",
                    derivative       = "forces",
                    mean             = means_energy,
                    stddev           = stddevs_enegy,
                    negative_dr      = True,
                )
                output_modules.append(ENERGY_FORCE)

            if "dipole_moment" in self.training_properties:

                DIPOLE_MOMENT = spk.atomistic.DipoleMoment(
                    n_in              = representation.n_atom_basis,
                    n_layers          = self.n_layers_dipole_moment,  # 2 -- default
                    n_neurons         = self.n_neurons_dipole_moment, # None -- default
                    activation        = spk.nn.activations.shifted_softplus,
                    property          = "dipole_moment",
                    contributions     = None,
                    predict_magnitude = False,
                    mean              = None,
                    stddev            = None,
                )
                output_modules.append(DIPOLE_MOMENT)

            print_function(f"Output_modules [{len(output_modules)}]: {output_modules}")

            self.model = AtomisticModel(representation, output_modules)
            print_function(f"Model parameters: {self.model}")

            self.model = torch.nn.DataParallel(self.model)
            print_function(f"{self.internal_name} [model building] done.")


    def build_trainer(self) -> None:

        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)

        # construct hooks # MeanSquaredError OR# RootMeanSquaredError
        metrics = [MeanAbsoluteError(p, p) if p != "forces" else MeanAbsoluteError(p, p, element_wise=True) for p in self.training_properties]

        hooks   = [
            CSVHook(log_path=self.model_path, metrics=metrics),
            ReduceLROnPlateauHook(optimizer, patience=5, factor=0.8, min_lr=1e-6, stop_after_min=True)
        ]

        # trainer
        loss = build_mse_loss(self.training_properties, loss_tradeoff=self.loss_tradeoff)
        self.trainer = Trainer(
            model_path        = self.model_path,
            model             = self.model,
            hooks             = hooks,
            loss_fn           = loss,
            optimizer         = optimizer,
            train_loader      = self.train_loader,
            validation_loader = self.valid_loader,
        )

    def _train(self, epochs:int = None, indexes:str = None, xyz_file:str = None) -> None:
        print_function(f"{self.internal_name} Training...")

        for epoch in tqdm(range(epochs), file=sys.stdout):
            epochs_done = self.storer.get(self.name4storer)

            if epoch <= epochs_done: continue
            else:
                # Training
                self.trainer.train(device=self.device, n_epochs=1)
                if epoch > 1 and self.plot_enabled: self.plot_training_progress()

                # Storing checkpoint
                self.storer.put(what=epochs_done+1, name=self.name4storer)
                self.storer.dump()

                if epoch % self.predict_each_epoch == 0 and epoch != 0:
                    if self.compare_with_foreign_model: self.predict(indexes=indexes, xyz_file=xyz_file, path2foreign_model=self.path2foreign_model)
                    self.predict(indexes=indexes, xyz_file=xyz_file, epochs_done=epoch)
                    self.use_model_on_test(db_name=indexes)

        # Show the last epoch
        self.predict(indexes=indexes, xyz_file=xyz_file, epochs_done=epochs)
        print_function(f"{self.internal_name} [model training] done.")

    def visualize_interest_region(self, indexes:str = None, samples4showing:int = 1, source_of_points:List[Atoms] = None, xyz_file:str = None) -> None:
        print_function(f"{self.internal_name} Visualizing regions of interest...")
        # visualization whole range of points
        if xyz_file:
            self.prepare_databases(redo=False, index=indexes, xyz_file=xyz_file)
            source_of_points = AtomsData(self.db_path + xyz_file+"_"+indexes+".db", load_only=self.training_properties)
        # end
        current_energy = []

        try:     start_region_of_interest, end_region_of_interest, step = [int(val) for val in indexes.split(":")]  # interval of interest
        except:  start_region_of_interest, end_region_of_interest       = [int(val) for val in indexes.split(":")]  # interval of interest without step
        num_samples = len(source_of_points)

        if samples4showing > num_samples:
            print_function(f"Warning! You requested samples for showing: {samples4showing}, however available only {num_samples}.")
            samples4showing = num_samples

        # choose number of points from the train data of region of interest
        idx_samples = [int(i) for i in np.linspace(0, num_samples-1, samples4showing)]

        for idx in idx_samples:
            _, props = source_of_points.get_properties(idx)
            current_energy.append(props['energy'][0])
        y = np.array(current_energy)
        x = [int(i) for i in np.linspace(start_region_of_interest, end_region_of_interest, samples4showing)]
        if not self.using_matplotlib:
            self.plotter_progress.plot(x=x, y=y,        key_name="data: train/showed:["+str(num_samples)+"/"+str(samples4showing)+"] total:" + str(len(self.samples)), page="xyz_file")
            self.plotter_progress.plot(x=x, y=(y-y[0]), key_name="data: train/showed:["+str(num_samples)+"/"+str(samples4showing)+"] total:" + str(len(self.samples)), page="xyz_file_sub")

    def train_model(self) -> None:
        """
        Main procedure of the training of neural network.

        """

        for xyz_file in self.db_epochs:
            print_function(f"XYZ data: {xyz_file}")
            for indexes, epochs in self.db_epochs[xyz_file].items():
                print_function(f"Indexes: {indexes}")
                self.prepare_databases(redo=False, index=indexes, xyz_file=xyz_file)
                self.prepare_train_valid_test_samples(db_name = xyz_file+"_"+indexes+".db")
                if self.plot_enabled: self.visualize_interest_region(indexes=indexes, samples4showing=self.visualize_points_from_data, source_of_points=self.train_samples)

                # creating model instance: creating representation, output_modules for it
                self.build_model()

                # initial preparations
                self.build_trainer()
                #
                self.name4storer = self.network_name +"_"+xyz_file+"_"+indexes+".nn"
                if not self.storer.get(self.name4storer): self.storer.put(what=0, name=self.name4storer)
                print_function(f"--> [Storer]  epochs done: {self.storer.show(get_string=True)}")
                print_function(f"--> [Trainer] epochs done: {self.trainer.epoch}")

                #
                self._train(epochs=epochs, indexes=indexes, xyz_file=xyz_file)
                self.use_model_on_test(db_name=indexes)

    def predict(self, indexes:str  = None, xyz_file:str = None, epochs_done:int = None, path2foreign_model:str = None) -> None:
        """
        Prediction method.

        Input:
        - indexes     [None] -- XX:XX:XX indexes for start / end / step
        - xyz_file    [None] -- path to xyz file
        - epochs_done [None] -- int used in plotting (optional)
        - path2foreign_model [None]  -- if set used for comparing
        """
        if 'dipole_moment' in self.training_properties or self.meta:
            """
            * No prodiction for dipole moment yet.
            * No need to predict anything on the remote job
            """
            return
        else:

            if path2foreign_model is not None:
                if not self.foreign_plotted: self.foreign_plotted = True
                network_name = key_prefix = "foreign_model"
                model_path   = path2foreign_model
                fname_name   = "before_energy_predicted_"+str(indexes)+".dat"
                epochs_done  = "[UNKNOWN]"
            else:
                network_name = key_prefix = str(self.network_name)
                model_path   = self.model_path
                fname_name   = "before_energy_predicted_"+str(indexes)+"_epochs"+str(epochs_done)+"_each"+str(self.visualize_each_point_from_nn)+"sample.dat"

            print_function(f"{self.internal_name} Prediction check [{network_name}]")
            step = None
            try:    start_region_of_interest, end_region_of_interest, step = [int(val) for val in indexes.split(":")]  # interval of interest
            except: start_region_of_interest, end_region_of_interest       = [int(val) for val in indexes.split(":")]  # interval of interest without step
            print_function(f"Region of interest: [start:{start_region_of_interest}|end:{end_region_of_interest}|step:{step}]")
            print_function(f"Visualization of each {self.visualize_each_point_from_nn}th sample...")

            # creating folder for model test
            test_path = os.path.join(self.test_path, network_name); os.makedirs(test_path, exist_ok=True)
            fname     = os.path.join(test_path, fname_name)

            if not os.path.exists(fname):
                initial_predicted_energy = []

                print_function(f"Reading {xyz_file}...")
                samples = read(self.xyz_path + xyz_file, index=indexes, format="extxyz")
                num_samples = len(samples)
                print_function(f"Num samples: {num_samples}")

                print_function(f"[{network_name}] Loading the last best model")
                best_model = torch.load(os.path.join(model_path, 'best_model'))

                calc = spk.interfaces.SpkCalculator(
                        model=best_model,
                        device=self.device,
                        energy='energy',
                        forces='forces',
                        environment_provider=spk.environment.AseEnvironmentProvider(6.)
                        )

                print_function(f"Predicting...")
                for idx_sample in tqdm(range(0,num_samples,self.visualize_each_point_from_nn)):
                    sample = samples[idx_sample]
                    if 'energy'        in self.training_properties: true_energy = sample.get_potential_energy()
                    if 'dipole_moment' in self.training_properties: true_dipole = sample.get_dipole_moment()
                    sample.set_calculator(calc)
                    initial_predicted_energy.append( (true_energy, sample.get_potential_energy()) )
                np.savetxt(fname, X=np.array(initial_predicted_energy))

            initial_predicted_energy = np.loadtxt(fname)
            # Plotting
            y      = initial_predicted_energy[:, 1]  # take predicted energy
            y_diff = initial_predicted_energy[:, 0] - initial_predicted_energy[:, 1]  # 'correct' - predicted energies
            x      = [int(i) for i in np.linspace(start_region_of_interest, end_region_of_interest, len(y)-2 )]  # TODO CHECK INDEXES

            if not self.using_matplotlib and self.plot_enabled:
                key_name = key_prefix+" epoch:"+str(epochs_done) + " predicted:" + str(len(y))
                self.plotter_progress.plot(x=x, y=y,        key_name=key_name, page="xyz_file")
                self.plotter_progress.plot(x=x, y=(y-y[0]), key_name=key_name, page="xyz_file_sub")
                self.plotter_progress.plot(x=x, y=y_diff,   key_name=key_name, page="e_diff")

    def use_model_on_test(self, db_name:str = None, path2model:str = None,) -> None:
        """
        The function provides ability to use model [trained/foreign] on the test data.

        """

        which = "trained" if path2model is None else "[FOREIGN]"
        if path2model is None: best_model = torch.load(os.path.join(self.model_path, 'best_model'))
        else:                  best_model = torch.load(os.path.join(path2model,      'best_model'))
        #print_function(f"{self.internal_name} Using the {which} model on the test data...")

        energy_error, forces_error, dipole_moment_error  = 0.0, torch.Tensor([.0, .0, .0]), torch.Tensor([.0, .0, .0])

        if self.test_loader is None: self.prepare_train_valid_test_samples(db_name=db_name)

        if "energy"        in self.training_properties: batch_name = "energy"
        if "dipole_moment" in self.training_properties: batch_name = "dipole_moment"

        samples_to_account = 0
        for _, batch in enumerate(self.test_loader):

            samples_to_account += len(batch[batch_name])
            # move batch to GPU, if necessary
            batch = {k: v.to(self.device) for k, v in batch.items()}

            # apply model
            pred = best_model(batch)

            if "energy" in self.training_properties:
                # calculate absolute error of energies
                tmp_energy    = torch.sum(torch.abs(pred["energy"] - batch["energy"]))
                tmp_energy    = tmp_energy.detach().cpu().numpy() # detach from graph & convert to numpy
                energy_error += tmp_energy

            if "forces" in self.training_properties:
                # calculate absolute error of forces, where we compute the mean over the n_atoms x 3 dimensions
                tmp_forces = torch.mean ( torch.mean(torch.abs(pred["forces"] - batch["forces"]), dim=(0)) , dim=(0,) )
                tmp_forces    = tmp_forces.detach().cpu().numpy() # detach from graph & convert to numpy
                forces_error += tmp_forces

            if "dipole_moment" in self.training_properties:
                # calculate absolute error of dipole_moment vector mean: n_atoms x 3 dimensions
                tmp_dipole_moment = torch.mean(torch.abs(pred["dipole_moment"] - batch["dipole_moment"]), dim=(0,))
                tmp_dipole_moment = tmp_dipole_moment.detach().cpu().numpy()
                dipole_moment_error += tmp_dipole_moment

        # division by number of samples
        energy_error        /= samples_to_account
        forces_error        /= samples_to_account
        dipole_moment_error /= samples_to_account

        print_function(f"""

Test MAE | epochs {self.storer.get(self.name4storer)}:
          <energy> [Hartree]          : {energy_error}
          <forces> [Hartree/angstrom] : {forces_error}
          <dipole moment> [Debye]     : {dipole_moment_error}

        """)

    def prepare_network(self, redo:bool = False) -> None:
        self.create_model_path(redo=redo)
        self.print_info()
        self.train_model()

