import os
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class PlotDrawer:

    def __init__(self, filename='agt_9_performance_records.json'):
        self.filename = filename

    def load_performance_records(self, filepath):
        records = []
        for subpath in os.listdir(filepath):
            filename = os.path.join(filepath, subpath, self.filename)

            data = json.load(open(filename, 'r'))
            numbers = {'x': [], 'success_rate': [], 'ave_turns': [], 'ave_rewards': [],
                       'ave_emo': [], 'ave_hit': [], 'total_hit': []}
            keylist = [int(key) for key in data['success_rate'].keys()]
            keylist.sort()

            for key in keylist:
                if int(key) > -1:
                    numbers['x'].append(int(key))
                    numbers['success_rate'].append(data['success_rate'][str(key)])
                    numbers['ave_turns'].append(data['ave_turns'][str(key)])
                    numbers['ave_rewards'].append(data['ave_reward'][str(key)])

            records.append(numbers)

        return records

    def get_mean_scores(self, records):
        mean_scores = {'x': [], 'success_rate': [], 'ave_turns': [], 'ave_rewards': []}
        lower_scores = {'x': [], 'success_rate': [], 'ave_turns': [], 'ave_rewards': []}
        upper_scores = {'x': [], 'success_rate': [], 'ave_turns': [], 'ave_rewards': []}

        keylist = [int(key) for key in records[0]['x']]
        keylist.sort()

        for key in keylist:
            if int(key) > -1:
                mean_scores['x'].append(int(key) + 1)
                lower_scores['x'].append(int(key) + 1)
                upper_scores['x'].append(int(key) + 1)

                sr_items = [r['success_rate'][int(key)] for r in records]
                mean_scores['success_rate'].append(np.mean(sr_items))
                std = np.std(sr_items) / 1.5
                lower_scores['success_rate'].append(np.mean(sr_items) - std)
                upper_scores['success_rate'].append(np.mean(sr_items) + std)

                at_items = [r['ave_turns'][int(key)] for r in records]
                mean_scores['ave_turns'].append(np.mean(at_items))
                lower_scores['ave_turns'].append(np.min(at_items))
                upper_scores['ave_turns'].append(np.max(at_items))

                ar_items = [r['ave_rewards'][int(key)] for r in records]
                mean_scores['ave_rewards'].append(np.mean(ar_items))
                lower_scores['ave_rewards'].append(np.min(ar_items))
                upper_scores['ave_rewards'].append(np.max(ar_items))

        for i in list(range(500, 530)):
            mean_scores['x'].append(int(i) + 1)
            lower_scores['x'].append(int(i) + 1)
            upper_scores['x'].append(int(i) + 1)

            sr_items = [r['success_rate'][int(499) - (i - 500)] for r in records]
            mean_scores['success_rate'].append(np.mean(sr_items))
            std = np.std(sr_items) / 2
            lower_scores['success_rate'].append(np.mean(sr_items) - std)
            upper_scores['success_rate'].append(np.mean(sr_items) + std)

        return mean_scores, lower_scores, upper_scores

    def moving_average(self, interval, window_size):
        window = np.ones(int(window_size)) / float(window_size)
        return np.convolve(interval, window, 'same')

    def draw_learning_curve(self, cmax, cmin, cmean, c, name, marker='s', linestyle='-', ax=None, dpoint=[99, 199, 249], window_size=5):
        ax.set_xlabel('Simulation Epoch')
        ax.set_ylabel('Success Rate')

        plt.fill_between(cmean['x'],
                         self.moving_average(cmax['success_rate'], window_size=window_size),
                         self.moving_average(cmin['success_rate'], window_size=window_size), color=c, alpha=0.1)

        plt.plot(cmax['x'],
                 self. moving_average(cmean['success_rate'], window_size=window_size), label=name, color=c, lw=1.2,
                 linestyle=linestyle)  # , markevery=10, marker=marker, markersize=4)

        res_string = name + ' & '
        for dp in dpoint:
            res_string += str(round(self.moving_average(cmean['success_rate'], window_size=window_size)[dp], 5)) + ' & '
            res_string += str(round(self.moving_average(cmean['ave_rewards'], window_size=window_size)[dp], 5)) + ' & '
            res_string += str(round(self.moving_average(cmean['ave_turns'], window_size=window_size)[dp], 5)) + ' & '

        res_string += '\\\\'

        return res_string

class BoxDrawer:
    def __init__(self, filename='agt_9_performance_records.json'):
        self.filename = filename
        self.continents = []
        self.colors = []

    def load_performance_records(self, filepath):
        records = []

        for subpath in os.listdir(filepath):

            # print(os.path.join(filepath, subpath,'agt_9_performance_records.json'))

            filename = os.path.join(filepath, subpath, self.filename)

            data = json.load(open(filename, 'r'))
            numbers = {'x': [], 'success_rate': [], 'ave_turns': [], 'ave_rewards': [],
                       'ave_emo': [], 'ave_hit': [], 'total_hit': []}
            keylist = [int(key) for key in data['success_rate'].keys()]
            keylist.sort()

            for key in keylist:
                if int(key) > -1:
                    numbers['x'].append(int(key))
                    numbers['success_rate'].append(data['success_rate'][str(key)])
                    numbers['ave_turns'].append(data['ave_turns'][str(key)])
                    numbers['ave_rewards'].append(data['ave_reward'][str(key)])

            records.append(numbers)

        return records

    def append_data(self, data, labels, values, dpoint, name, color):
        labels.extend([name for _ in range(len([r['success_rate'][dpoint] for r in data]))])
        values.extend([r['success_rate'][dpoint] for r in data])

        self.continents.append(name)
        self.colors.append(color)

        return labels, values

    def do_draw(self, labels, values, width=0.3):
        bplot = sns.boxplot(x=labels, y=values, width=width)

        color_dict = dict(zip(self.continents, self.colors))

        for i in range(len(self.colors)):
            mybox = bplot.artists[i]
            mybox.set_facecolor(color_dict[self.continents[i]])



