# Core compilation requires neither shell escape nor Python. The no-dot filename
# latexmkrc is recognised by Overleaf. Select LuaLaTeX and the main .tex file there.
$pdf_mode = 4;
$max_repeat = 8;
$lualatex = 'lualatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error %O %S';
$pdflatex = 'pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error %O %S';

# imakeidx runs in noautomatic mode. latexmk discovers the named indexes from
# the log and invokes makeindex. Do not add an idx/ind custom dependency: it
# would duplicate latexmk's native multi-index rules.
# The internal callback uses Perl's list-form system, so makeindex's filenames
# and flags are arguments rather than a shell command.
# Run inside the output directory so absolute build paths remain compatible
# with MakeIndex's default restrictions on output filenames.
$makeindex_fudge = 1;
$makeindex = 'internal law_makeindex %O -o %D %S';
sub law_makeindex {
    return system('makeindex', @_);
}

push @generated_exts, 'idx', 'ind', 'ilg';
