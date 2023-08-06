from typing import Tuple
from statistics import mean, median, stdev
from modular_towers import mod_tower as modtow
from modular_towers.testing import benchmark, rand_n_digit_int, dot_to_and

def test_core(
    list_lengths: Tuple[int],
    bit_lengths: Tuple[int],
    mod_bit_lengths: Tuple[int],
    num_iters: int = 1000,
    max_seconds: int = None,
    latex: bool = False
):
    if latex:
        print('\\begin{tabular}{cc|%s}' % ('r@{.}l'*len(list_lengths)*2))
        print('\t\\toprule')
        print('\t& \\multicolumn{1}{c}{} & \\multicolumn{%d}{c}{sequence length $\\ell$} \\\\' % (len(list_lengths)*4))
        print('\t& \\multicolumn{1}{c}{} & %s \\\\' % ' & '.join(['\\multicolumn{4}{c}{$%d$}' % l for l in list_lengths]))
        print('\t%s' % ' '.join(['\\cmidrule(r){%d-%d}' % (4*i+3,4*i+6) for i in range(len(list_lengths))]))
        print('\t$B$ & \\multicolumn{1}{c}{$b$} & %s \\\\' % ' & '.join(['\\multicolumn{2}{c}{mean} & \\multicolumn{2}{c}{stdev}' for _ in list_lengths]))
    
    for Bm in mod_bit_lengths:
        if latex:
            print('\t\\midrule')
            print('\t\\multirow{%d}{*}{$%d$}' % (len(bit_lengths), Bm))
        for Ba in bit_lengths:
            if latex:
                print('\t\t& $%d$ ' % Ba, end='')
            for l in list_lengths:
                args = (([rand_n_digit_int(Ba) for _ in range(l)], rand_n_digit_int(Bm)) for _ in range(num_iters))
                times = benchmark((modtow,), args, max_seconds=max_seconds)[modtow]
                if latex:
                    print('& %s & %s' % (dot_to_and('%.2f'%(mean(times)*1000)), dot_to_and('%.2f'%(stdev(times)*1000))), end='')
            if latex:
                print(' \\\\')
    
    if latex:
        print('\t\\bottomrule')
        print('\\end{tabular}')