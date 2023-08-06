import tensorflow as tf
import os
import numpy as np
import functools

import gym

import chainer
import chainerrl
from chainerrl import links
from chainerrl import policies
from chainerrl import v_functions
from chainerrl.agents import a3c
from chainer import optimizers
from chainerrl import agents
from chainerrl import misc
from chainerrl import replay_buffer
from chainerrl.q_functions import DistributionalDuelingDQN
from chainerrl.q_functions import DistributionalFCStateQFunctionWithDiscreteAction
from chainerrl.action_value import DiscreteActionValue
from chainerrl.distribution import SoftmaxDistribution
import chainer.functions as F
import chainer.links as L


class AtariAgent():
    def action_order(self, obs):
        if self.alg == "DQN-C" or self.alg == "Rainbow" or self.alg == "IQN":
            with chainer.using_config('train', False), chainer.no_backprop_mode():
                action_value = \
                    self.agent._evaluate_model_and_update_recurrent_states([obs], test=True)
                qvalues = action_value.q_values.array
                return np.argsort(-qvalues[0]).astype(np.int32)
        if self.alg == "A3C":
            with chainer.no_backprop_mode():
                statevar = self.agent.batch_states([obs], np, self.agent.phi)
                pout, _ = self.agent.model.pi_and_v(statevar)
                return np.argsort(-pout.all_prob.array[0]).astype(np.int32)
        if self.alg == "ACER":
            statevar = np.expand_dims(self.agent.phi(obs), 0)
            action_distrib, _, _ = self.agent.model(statevar)
            return np.argsort(action_distrib.all_prob.array, axis=1).astype(np.int32)

    def act(self, obs):
        return self.agent.act(obs)

    def __init__(self, alg, env, model_path):
        self.alg = alg
        seed = 0
        n_actions = gym.make(env).action_space.n
        gpus = [-1]
        gpu = None
        misc.set_random_seed(seed, gpus=gpus)
        if alg == "DQN-C":
            model = links.Sequence(
                links.NatureDQNHead(),
                L.Linear(512, n_actions),
                DiscreteActionValue)
        if alg == "PPO":
            winit_last = chainer.initializers.LeCunNormal(1e-2)
            model = chainer.Sequential(
                L.Convolution2D(None, 32, 8, stride=4),
                F.relu,
                L.Convolution2D(None, 64, 4, stride=2),
                F.relu,
                L.Convolution2D(None, 64, 3, stride=1),
                F.relu,
                L.Linear(None, 512),
                F.relu,
                links.Branched(
                    chainer.Sequential(
                        L.Linear(None, n_actions, initialW=winit_last),
                        SoftmaxDistribution,
                    ),
                    L.Linear(None, 1),
                )
            )
        if alg == "C51":
            n_atoms = 51
            v_max = 10
            v_min = -10
            model = links.Sequence(
                links.NatureDQNHead(),
                DistributionalFCStateQFunctionWithDiscreteAction(
                    None, n_actions, n_atoms, v_min, v_max,
                    n_hidden_channels=0, n_hidden_layers=0),
            )
        if alg == "ACER":
            model = agents.acer.ACERSharedModel(
                shared=links.Sequence(
                    links.NIPSDQNHead(),
                    L.LSTM(256, 256)),
                pi=links.Sequence(
                    L.Linear(256, n_actions),
                    SoftmaxDistribution),
                q=links.Sequence(
                    L.Linear(256, n_actions),
                    DiscreteActionValue),
            )
        if alg == "A3C":
            model = A3CFF(n_actions)
        if alg == "Rainbow":
            n_atoms = 51
            v_max = 10
            v_min = -10
            model = DistributionalDuelingDQN(n_actions, n_atoms, v_min, v_max)
            links.to_factorized_noisy(model, sigma_scale=0.5)
        if alg == "IQN":
            model = agents.iqn.ImplicitQuantileQFunction(
                psi=chainerrl.links.Sequence(
                    L.Convolution2D(None, 32, 8, stride=4),
                    F.relu,
                    L.Convolution2D(None, 64, 4, stride=2),
                    F.relu,
                    L.Convolution2D(None, 64, 3, stride=1),
                    F.relu,
                    functools.partial(F.reshape, shape=(-1, 3136)),
                ),
                phi=chainerrl.links.Sequence(
                    chainerrl.agents.iqn.CosineBasisLinear(64, 3136),
                    F.relu,
                ),
                f=chainerrl.links.Sequence(
                    L.Linear(None, 512),
                    F.relu,
                    L.Linear(None, n_actions),
                ),
            )
        if alg in ["A3C"]:
            fake_obs = chainer.Variable(
                np.zeros((4, 84, 84), dtype=np.float32)[None],
                name='observation')
            with chainerrl.recurrent.state_reset(model):
                # The state of the model is reset again after drawing the graph
                variables = misc.collect_variables([model(fake_obs)])
                chainer.computational_graph.build_computational_graph(variables)
        elif alg in ["Rainbow", "DQN-C", "C51", "ACER", "PPO"]:
            variables = misc.collect_variables([model(np.zeros((4, 84, 84), dtype=np.float32)[None])])
            chainer.computational_graph.build_computational_graph(variables)
        else:
            fake_obs = np.zeros((4, 84, 84), dtype=np.float32)[None]
            fake_taus = np.zeros(32, dtype=np.float32)[None]
            variables = misc.collect_variables([model(fake_obs)(fake_taus)])

        def phi(x):
            # Feature extractor
            return np.asarray(x, dtype=np.float32) / 255

        opt = optimizers.RMSpropGraves()
        opt.setup(model)
        rbuf = replay_buffer.ReplayBuffer(1)
        if alg == "IQN":
            self.agent = agents.IQN(model, opt, rbuf, gpu=gpu, gamma=0.99, act_deterministically=True, explorer=None,
                                    replay_start_size=1, minibatch_size=1, target_update_interval=None, clip_delta=True,
                                    update_interval=4, phi=phi)
        if alg == "A3C":
            self.agent = a3c.A3C(model, opt, t_max=5, gamma=0.99, phi=phi, act_deterministically=True)
        if alg == "Rainbow":
            self.agent = agents.CategoricalDoubleDQN(model, opt, rbuf, gpu=gpu, gamma=0.99, explorer=None,
                                                     replay_start_size=1, minibatch_size=1, target_update_interval=None,
                                                     clip_delta=True, update_interval=4, phi=phi)
        if alg == "DQN-C":
            self.agent = agents.DQN(model, opt, rbuf, gpu=gpu, gamma=0.99, explorer=None, replay_start_size=1,
                                    minibatch_size=1, target_update_interval=None, clip_delta=True, update_interval=4,
                                    phi=phi)
        if alg == "C51":
            self.agent = agents.CategoricalDQN(
                model, opt, rbuf, gpu=gpu, gamma=0.99,
                explorer=None, replay_start_size=1,
                minibatch_size=1,
                target_update_interval=None,
                clip_delta=True,
                update_interval=4,
                phi=phi,
            )
        if alg == "ACER":
            self.agent = agents.acer.ACER(model, opt, t_max=5, gamma=0.99,
                                          replay_buffer=rbuf,
                                          n_times_replay=4,
                                          replay_start_size=1,
                                          act_deterministically=True,
                                          phi=phi
                                          )
        if alg == "PPO":
            self.agent = agents.PPO(model, opt, gpu=gpu, phi=phi, update_interval=4, minibatch_size=1, clip_eps=0.1,
                                    recurrent=False, act_deterministically=True)
        self.agent.load(os.path.join(model_path, 'chainer', alg, env.replace("NoFrameskip-v4", ""), 'final'))


class A3CFF(chainer.ChainList, a3c.A3CModel):

    def __init__(self, n_actions):
        self.head = links.NIPSDQNHead()
        self.pi = policies.FCSoftmaxPolicy(
            self.head.n_output_channels, n_actions)
        self.v = v_functions.FCVFunction(self.head.n_output_channels)
        super().__init__(self.head, self.pi, self.v)

    def pi_and_v(self, state):
        out = self.head(state)
        return self.pi(out), self.v(out)
