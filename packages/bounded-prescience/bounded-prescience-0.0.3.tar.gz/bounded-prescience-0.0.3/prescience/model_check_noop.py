import gym
import numpy as np
import time
import copy
from prescience import get_wrapped
from collections import deque
from gym.wrappers import Monitor


def check_noops(env_str, method_str, prop_str, action_function, max_noops=29, render=False, max_frames=100000,
                verbose=False, min_noops=0, shield=0, demand_full_safety=False, record=False):
    env = get_wrapped(env_str, method_str, prop_str)
    if record:
        env = Monitor(env, "recording", force=True, video_callable=lambda episode_id: True)
    violation_list = []
    noop_violation_list = []
    reward_list = []
    if verbose:
        print('Checking if %s ever violates %s in %s, with a lookahead of %d' % (method_str, prop_str, env_str, shield))
    start = time.time()
    for i in range(min_noops, max_noops):
        if verbose:
            print('Running with %d noops' % i)
        checker = ModelChecker(action_function, env, env.action_space.n, i, shield=shield, render=render,
                               verbose=verbose, max_frames=max_frames)
        output = None
        while output == None:
            output = checker.step()
        violation_list.append(output[0])
        noop_violation_list.append(output[1])
        reward_list.append(output[2])
        if output[0] != "None" and demand_full_safety:
            if verbose:
                print("Found unsafe trace, property not fully satisfied.")
            break
        if verbose:
            print("Steps taken during run: %d. Time taken: %d" % (output[3], time.time() - start))
    if verbose:
        print("Finished checking traces in %d seconds" % (time.time() - start))
    env.close()
    return violation_list, noop_violation_list, reward_list


class ModelChecker():
    def __init__(self, action_function, env, actions, noops, shield=0, render=False, verbose=False, max_frames=10000,
                 action_repeat=0):
        self.render = render
        self.get_order = action_function
        self.env = env
        self.num_actions = actions
        self.shield = shield
        self.history = []
        self.tot_reward = 0
        self.frame = 0
        self.violation = "None"
        self.noop_violation = "None"
        self.noops = noops
        self.verbose = verbose
        self.max_frames = max_frames
        self.next_action = 0
        self.stored_action = None
        self.action_repeat = action_repeat
        obs = self.env.reset()
        action_list = self.get_order(obs)
        state = self.env.save()
        self.history.append(HistoryEntry(state, action_list, 0, 0))

    def commit_step(self):
        entry = self.history.pop(0)
        self.tot_reward += entry.reward

    def get_action(self):
        if self.next_action != 0:
            self.next_action -= 1
            return self.stored_action
        if self.frame <= self.noops:
            self.stored_action = 0
            self.next_action = self.action_repeat
            return 0
        else:
            current = self.history[-1]
            self.stored_action = current.action_list[current.index]
            self.next_action = self.action_repeat
            return current.action_list[current.index]

    def evaluate_step(self):
        if self.render:
            self.env.render()
        obs, reward, done, info = self.env.step(self.get_action())
        if (self.frame > self.noops and self.violation != "None") or (
                self.frame <= self.noops and self.noop_violation != "None"):
            info['label'] = False
        return obs, reward, done, info['label']

    def take_step(self, obs, reward):
        action_list = self.get_order(obs)
        state = self.env.save()
        self.history.append(HistoryEntry(state, action_list, 0, reward))
        self.frame += 1

    def next_best(self):
        while len(self.history) > 1 and self.history[-1].index >= self.num_actions - 1:
            self.history.pop()
            self.frame -= 1
        new = self.history[-1]
        new.increment_index()
        if new.index >= self.num_actions:
            assert len(self.history) == 1
            new.index = 0
            self.record_violation()
        self.env.restore(new.state)

    def record_violation(self):
        if self.verbose:
            print('Property violated in all possible %d lookaheads from step %d' % (self.shield, self.frame))
        if self.frame <= self.noops:
            self.noop_violation = self.frame
        else:
            self.violation = self.frame

    def end(self):
        while len(self.history) > 0:
            self.commit_step()
        return self.violation, self.noop_violation, self.tot_reward, self.frame

    def max_lookahead(self):
        return len(self.history) >= self.shield

    def step(self):
        obs, reward, done, unsafe = self.evaluate_step()  # evaluates result of taking step
        if unsafe and self.shield > 0:
            self.next_best()  # switches to next-best option (estimated by policy) among possible deviations up to $shield steps back. Logs a violation if no other options remain.
        else:
            if unsafe:
                self.record_violation()  # only reached with no shielding
            if self.max_lookahead():  # the oldest non-commited action can be safely commited since full lookahead has been done.
                self.commit_step()  # commits the oldest action, such that it can no longer be retracted
            self.take_step(obs,
                           reward)  # takes the evaluated step, but stores the state and can be retracted until the step is committed
            if done or self.frame > self.max_frames:
                return self.end()
        return None


class HistoryEntry():
    def __init__(self, state, action_list, index, reward):
        self.state = state
        self.action_list = action_list
        self.index = index
        self.reward = reward

    def increment_index(self):
        self.index += 1
