import os
import numpy as np
import pandas as pd
from bgNetwork.analyzefx import *
from scipy.stats.distributions import norm
from scipy.stats import truncnorm
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.simplefilter('ignore', np.RankWarning)

roundRT = lambda x, ndec: int(round(float(str(x)[:5]), ndec)*1000)



def plot_behavior(empdata, simdata, labels=['low', 'med', 'high'], simclrs=['#2876B9'], simlabels=['Drift']):

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5,4.5))
    x = np.arange(1, len(labels)+1)
    xtl = labels
    rtemp, rtempErr, accemp, accempErr = empdata
    ax1.errorbar(x, rtemp, yerr=rtempErr, marker='o', markersize=8, linewidth=2.5, elinewidth=2.5, color='k', mec='k', mew=2,label='CBGT Network')
    ax2.errorbar(x, accemp, yerr=accempErr, marker='o', markersize=8, linewidth=2.5, elinewidth=2.5, color='k', mec='k', mew=2)

    for i, simd in enumerate(simdata):
        rtsim, rtsimErr, accsim, accsimErr = simd
        c = simclrs[i]
        l = simlabels[i]
        ax1.errorbar(x+.04, rtsim, yerr=rtsimErr, mfc=c, marker='o', markersize=6,
                     linewidth=2., elinewidth=2.5, mec=c, mew=2, color=c, label=l)
        ax2.errorbar(x+.04, accsim, yerr=accsimErr, mfc=c, marker='o', markersize=6,
                     linewidth=2., elinewidth=2.5, mec=c, mew=2, color=c)

    for ax in [ax1, ax2]:
        ax.set_xlim(x[0]-.2, x[-1]+.2)
        ax.set_xticks(x)
        ax.set_xticklabels(xtl)
    yt=np.arange(.20, .45, .05)
    ax1.set_yticks(yt)
    ax1.set_yticklabels([int(round(ytl,2)) for ytl in yt*1000])
    ax2.set_yticks(np.arange(.4, 1.1, .1))
    ax2.set_ylim(.4, 1.05)
    ax1.set_ylabel('RT (ms)')
    ax2.set_ylabel('Accuracy')
    ax1.set_xlabel('D/I Ratio (All Channels)')
    ax2.set_xlabel('D/I Ratio (All Channels)')
    ax1.legend()
    sns.despine()
    plt.tight_layout()


def plot_mean_acc_rt(df, conds=['low', 'med', 'high']):


    clrs = ['#febe08', '#00bac7', '#347fff'][::-1]
    #eclrs = ['#eb9632', '#00928c', '#143773'][::-1]
    eclrs = ['#f5a005', '#009c82', '#1657de'][::-1]
    pal = sns.color_palette(eclrs)

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5,4.85))
    if 'trial' in df.columns:
        dfacc = df[df.trial>150]
    else:
        dfacc = df.copy()
    ax1 = sns.pointplot(x='level', y='acc', data=dfacc, palette=pal, order=[1,2,3], scale=1.65, errwidth=3, ax=ax1, ci=99)
    ax2 = sns.pointplot(x='level', y='rtms', data=df[df.acc==1], palette=pal, order=[1,2,3], scale=1.65, errwidth=3, ax=ax2, ci=99)

    x = [0,1,2]
    yacc = dfacc.groupby('level').mean()['acc'].values
    yrt =  df[df.acc==1].groupby('level').mean()['rtms'].values

    ax1.plot(x, yacc, linewidth=5, alpha=.25, color='k')
    ax2.plot(x, yrt, linewidth=5, alpha=.25, color='k')

    for i in range(3):
        ax1.plot([i], [yacc[i]], color=clrs[i], marker='o', linewidth=0, mfc=clrs[i], mew=2, mec=eclrs[i], ms=12)
        ax2.plot([i], [yrt[i]],  color=clrs[i], marker='o', linewidth=0, mfc=clrs[i], mew=2, mec=eclrs[i], ms=12)

    for ax in [ax1, ax2]:
        ax.set_xticks(range(len(conds)))
        ax.set_xticklabels([c.capitalize() for c in conds])
        ax.set_xlabel('P(rew | Left)')
        sns.despine(ax=ax)

    ax1.set_ylim(.4, 1.025)
    #ax2.set_ylim(440, 500)
    #ax2.set_yticks(np.arange(440,520,20))
    ax1.set_yticks([.4, .6, .8, 1.])
    ax1.set_yticklabels([.4, .6, .8, 1.])
    ax1.set_ylabel('Accuracy')
    ax2.set_ylabel('RT (ms)')
    plt.tight_layout()


def plot_cond_rtdist(bdf, bins=12, outdir=None, cond='low', norm_hist=False):
    #splot.style(fscale=1.3)
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(8,3), sharey=True)
    sns.distplot(bdf[bdf.acc==1].rtms.values, color='k', ax=ax1, kde=False,
                 norm_hist=norm_hist, label='Left', bins=bins)
    if bdf[bdf.acc==0].shape[0] > 2:
        sns.distplot(bdf[bdf.acc==0].rtms.values, color='r', ax=ax2, kde=False,
                     norm_hist=norm_hist, label='Right', bins=int(bins/2))
        ax2.legend()
    f.suptitle(cond.capitalize())
    sns.despine(); plt.tight_layout
    ax1.set_ylabel('Probability Density')
    ax1.set_xlabel('RT (ms)')
    ax2.set_xlabel('RT (ms)')
    ax1.legend()
    for i, ax in enumerate([ax2, ax1]):
        ax.set_yticklabels([])
        xmin, xmax = [roundRT(xx, 2) for xx in [bdf.rt.min(), bdf.rt.max()]]
        ax.set_xticks(np.arange(xmin, xmax+100, 100))
        ax.set_xticklabels(np.arange(xmin, xmax+100, 100))
        ax.set_xlim(xmin-20, xmax)
    plt.tight_layout()
    if outdir is not None:
        plt.savefig(os.path.join(outdir, '{}_rt_dists.png'.format(cond)), dpi=400)


def plot_cor_err_rts(bdf, bins=12, outdir=None, norm_hist=False):
    f, ax = plt.subplots(1, figsize=(6.5,3.9))
    cond = bdf.cond.iloc[0]
    sns.distplot(bdf[bdf.acc==1].rtms.values, label='Left', color='Green', bins=bins, kde=False, ax=ax, norm_hist=norm_hist)
    ax = sns.distplot(bdf[bdf.acc==0].rtms.values, label='Right', color='Red', bins=int(bins/2), kde=False, ax=ax, norm_hist=norm_hist)
    ax.legend(); ax.set_title(cond.capitalize()); sns.despine()
    xmin=roundRT(bdf.rt.min(), 2); xmax=roundRT(bdf.rt.max(), 2)
    ax.set_xlim(xmin-25, xmax+50)
    ax.set_yticklabels([])
    ax.set_ylabel('Probability Density')
    ax.set_xlabel('RT (ms)')
    plt.tight_layout()
    if outdir is not None:
        plt.savefig(os.path.join(outdir, '{}_cor_err_rt_dists.png'.format(cond)), dpi=400)


def plot_stim_dist(mu=2.49, sd=.025, clip=None, ntrials=1000, bins=25):
    if clip is not None:
        lower, upper = clip[0], clip[1]
        a = (lower - mu) / sd
        b = (upper - mu) / sd
        stimArray = truncnorm(a, b, loc=mu, scale=sd).rvs(ntrials)
    else:
        stimArray = norm(mu, sd).rvs(ntrials)
    _=plt.hist(stimArray, bins=bins); sns.despine()
    return stimArray


def plot_average_msn_rates(ys, ysErr, bdf, ntime=500, plotRT=False, plotRTerr=False, outdir=None):

    f, axes = plt.subplots(2, 3, figsize=(10, 6), sharey=False, sharex=False)
    axes = np.asarray(axes).reshape(2,3)
    lrclrs=['#1e1e1e', '#f5191c']
    titles = ['Low', 'Med', 'High']
    lrEclrs = ['#b0b0b0', '#f9aeb0']
    clrs = ['#feb408', '#00bac7', '#3b73d4'][::-1]
    eclrs = ['#eb9632', '#00928c', '#143773'][::-1]
    eclrs = ['#eb9632', '#009c96', '#143773'][::-1]

    clrs = ['#febe08', '#00bac7', '#347fff'][::-1]
    eclrs = ['#f5a005', '#009c82', '#1657de'][::-1]
    pal = sns.color_palette(eclrs)


    pal = sns.color_palette(clrs)

    condRTs = bdf.groupby('cond2').mean()['rtms'].values.astype(int)
    rtErrs = bdf.groupby('cond2').std()['rtms'].values

    for i in range(3):
        lbl0, lbl1 = None, None
        xmax = condRTs[i]
        if i==0:
            lbl0, lbl1 = 'Left', 'Right'
        y0, y1, y2, y3 = [y[i, :xmax] for y in ys]
        e0, e1, e2, e3 = [e[i, :y0.size] for e in ysErr]
        x = np.arange(200, 200+y0.shape[0])

        axes[0, i].plot(x, y0, linewidth=3, color=lrclrs[0], label=lbl0, zorder=10)
        axes[0, i].plot(x, y1, linewidth=3, color=lrclrs[1], label=lbl1, zorder=10)
        axes[0, i].fill_between(x, y0-e0, y0+e0, color=lrEclrs[0], alpha=.5, zorder=5)
        axes[0, i].fill_between(x, y1-e1, y1+e1, color=lrEclrs[1], alpha=.5, zorder=5)

        axes[1, i].plot(x, y2, linewidth=3, color=lrclrs[0], zorder=10)
        axes[1, i].plot(x, y3, linewidth=3, color=lrclrs[1], zorder=10)
        axes[1, i].fill_between(x, y2-e2, y2+e2, color=lrEclrs[0], alpha=.5, zorder=5)
        axes[1, i].fill_between(x, y3-e3, y3+e3, color=lrEclrs[1], alpha=.5, zorder=5)


        if plotRT:
            rtLower = xmax-rtErrs[i]
            rtUpper = xmax+rtErrs[i]

            axes[0, i].vlines(xmax, 0, 45, linewidth=2.5, color=clrs[i], linestyle='-', alpha=.85, zorder=20)
            axes[1, i].vlines(xmax, 0, 45, linewidth=2.5, color=clrs[i], linestyle='-', alpha=.85, zorder=20)
            axes[0, i].plot([xmax], [45], linewidth=0, marker='o', ms=8, color=clrs[i], zorder=15)
            axes[1, i].plot([xmax], [45], linewidth=0, marker='o', ms=8, color=clrs[i], zorder=15)

            if plotRTerr:
                axes[0, i].fill_betweenx([0,45], [rtLower]*2,[rtUpper]*2, color=eclrs[i], alpha=.075, zorder=-10)
                axes[1, i].fill_betweenx([0,45], [rtLower]*2,[rtUpper]*2, color=eclrs[i], alpha=.075, zorder=-10)


    for ax in axes.flatten():
        ax.set_xticks(np.linspace(205, ntime+5, 5))
        ax.set_xlim(202, ntime)
        ax.set_ylim(3., 47)
        ax.set_yticks([3.5, 15, 30, 45])
        ax.set_yticklabels([0, 15, 30, 45])

        if ax.is_first_row():
            ax.set_xticklabels([])
        else:
            ax.set_xticks(np.linspace(210, ntime+10, 5))
            ax.set_xticklabels(['200', '', '', '', str(ntime)])

    _=axes[0,0].legend(loc=2)
    _=axes[0,0].set_ylabel('dMSN Rate (Hz)')
    _=axes[1,0].set_ylabel('iMSN Rate (Hz)')
    for i, ax in enumerate(axes[0, :]):
        ax.set_title(titles[i])
    for i, ax in enumerate(axes[1, :]):
        ax.set_xlabel('Time (ms)')
    sns.despine()
    plt.tight_layout()

    if outdir is not None:
        plt.savefig(os.path.join(outdir, 'DI_AvgRates_muRT.png'), dpi=600)


def plot_spikes(df, start=200, nchoices=2, clrs=['#1e1e1e', '#f5191c']):
    f, axes = plt.subplots(2, 4, figsize=(12,4.75), sharex=True)
    axes = axes.flatten()
    if isinstance(df, dict):
        df = df['popfreqs'].values
    pops = ['LIP', 'dMSN', 'iMSN', 'FSI', 'GPe', 'STN', 'GPi', 'Th']
    LIPb_ix = 1
    M1_ix = 2
    x = df.loc[start:, 'time'].values
    ymax=[]
    for i in range(nchoices):
        choicelabel = ['Left', 'Right'][i]
        for ii, pop in enumerate(pops):
            ax = axes[ii]
            label = pop.split('_')[0]
            if pop in ['FSI', 'LIPI']:
                y = df.loc[start:, pop].values
                ax.plot(x, y, color='k', linewidth=2.25)
                ax.set_title(label)
                if i == 0:
                    ymax.append([])
                else:
                    ymax[ii].append(np.nanmax(y))
                continue
            else:
                y = df.loc[start:, '{}{}'.format(pop, i)].values
                clr = clrs[i]
            if i == 0:
                ymax.append([])
            ax.plot(x, y, color=clr, label=choicelabel, linewidth=2.25)
            ax.set_title(label)
            ymax[ii].append(np.nanmax(y))
            if axes[ii].is_last_row():
                axes[ii].set_xlabel('Time (ms)')
    upper = [np.nanmax(ym)*1.08 for ym in ymax]
    for i, ymax in enumerate(upper):
        axes[i].set_ylim(0, ymax)
        if pops[i] == 'LIP':
            axes[i].legend(loc=2)
        if axes[i].is_first_col():
            axes[i].set_ylabel('Firing Rate (Hz)')
    plt.tight_layout()
    sns.despine()
    return f



def plot_trial_rates(t=0, cond='test'):
    pops = ['LIP0', 'LIPI', 'dMSN0', 'iMSN0', 'FSI',
            'GPeP0', 'GPi0', 'Th0']
    results = np.hstack(ng.readAllTrialResults(1,0,1))
    plotspikes = print_trial_acc_rt(results, t=t)
    if plotspikes:
        ratedf = results[t]['popfreqs']
        frdf2 = get_firing_rates(results, window=2, cond=cond)
        ratedfT = get_single_trial_ratedf(frdf2)
        titles=['Cortex', 'dMSN', 'iMSN', 'FSI', 'GPe',  'STN', 'GPi', 'Thalamus']
        yranges = [(0,25), (0,50), (0,50), (0,30), (0, 125), (0,70), (0, 125), (0, 30)]
        xmax = np.around(ratedf.index.values[-1], 1)
        xticks = np.arange(200, xmax+100, 100)
        fig = plot_spikes(ratedfT, start=200)
        axes = np.asarray(fig.axes).flatten()
        for i, ax in enumerate(axes):
            title = titles[i]
            ax.set_title(title)
            #ylow, yhigh = yranges[i]
            #ax.set_ylim(ylow, yhigh)
            #ax.set_yticks(np.linspace(ylow, yhigh, 5))
            #ax.set_yticklabels([str(ylow), '', '', '', str(yhigh)])
            ax.set_xticks(xticks)
            if ax.is_last_row():
                ax.set_xticks(xticks)
                ax.set_xticklabels(xticks)
        plt.tight_layout()


def save_and_plot(results, behavdf, cond='bal', savedir='~/cbgt', window=2, Start=200, trials=[None], getdfs=False, plot_avg=False):
    spikedf = get_firing_rates(results, window=window, cond=cond)
    avgRates = get_mean_firing_rates(spikedf)
    if trials[0] is not None:
        for t in trials:
            dftrial = get_single_trial_ratedf(spikedf, t)
            ftrial = plot_spikes(dftrial, start=Start)
            fname = 'rates_{}_trial{}.png'.format(cond, str(t))
            ftrial.savefig(os.path.join(savedir, fname), dpi=500)
        plt.close('all')

    if plot_avg:
        favg = plot_spikes(avgRates, start=Start)
        fname = 'rates_{}_avg.png'.format(cond)
        favg.savefig(os.path.join(savedir, fname), dpi=500)

    spikedfName = 'cbgt_spikedf_alltrials_{}.csv'.format(cond)
    avgRatesName = 'cbgt_spikedf_mean_{}.csv'.format(cond)
    spikedf.to_csv(os.path.join(savedir, spikedfName), index=False)
    avgRates.to_csv(os.path.join(savedir, avgRatesName), index=False)
    if getdfs:
        return spikedf, avgRates