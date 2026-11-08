% SPDX-License-Identifier: MIT
\NeedsTeXFormat{LaTeX2e}[2021-06-01]
\ProvidesClass{lawthesis}[2026/11/08 v1.0.0 LexThesis doctoral law template]
\newif\ifLawPrint
\newif\ifLawReview
\newif\ifLawAnonymous
\newif\ifLawGroningen
\newif\ifLawArticles
\DeclareOption{print}{\LawPrinttrue}
\DeclareOption{review}{\LawReviewtrue}
\DeclareOption{anonymous}{\LawAnonymoustrue\LawReviewtrue}
\DeclareOption{groningen}{\LawGroningentrue\LawPrinttrue}
\DeclareOption{articles}{\LawArticlestrue}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{scrbook}}
\ProcessOptions\relax
\ifLawPrint
  \PassOptionsToClass{twoside,openright}{scrbook}
\else
  \PassOptionsToClass{oneside,openany}{scrbook}
\fi
\LoadClass[12pt,headings=normal,parskip=false]{scrbook}
\RequirePackage{iftex}
\ifPDFTeX
  \RequirePackage[T1]{fontenc}
  \RequirePackage[utf8]{inputenc}
  \RequirePackage{lmodern}
\else
  \RequirePackage{fontspec}
  \setmainfont{Latin Modern Roman}
  \setsansfont{Latin Modern Sans}
  \setmonofont{Latin Modern Mono}[Scale=MatchLowercase]
\fi
\RequirePackage[dutch,british]{babel}
\RequirePackage{microtype}
\RequirePackage{geometry}
\ifLawGroningen
  \geometry{paperwidth=170mm,paperheight=240mm,inner=25mm,outer=20mm,top=22mm,bottom=24mm,headheight=18pt,headsep=7mm,footskip=12mm}
\else
  \geometry{a4paper,inner=35mm,outer=27mm,top=27mm,bottom=29mm,headheight=18pt,headsep=8mm,footskip=13mm}
\fi
\RequirePackage{setspace}
\ifLawReview\doublespacing\else\setstretch{1.22}\fi
\RequirePackage{xcolor}
\definecolor{LawInk}{HTML}{18314A}
\definecolor{LawMuted}{HTML}{49545F}
\definecolor{LawAccent}{HTML}{8B4A36}
\ifLawPrint
  \colorlet{LawInk}{black}\colorlet{LawAccent}{black}
\fi
\RequirePackage{graphicx}
\RequirePackage{pdfpages}
\RequirePackage{booktabs}
\RequirePackage{longtable}
\RequirePackage{tabularx}
\RequirePackage{enumitem}
\setlist{nosep,topsep=5pt,leftmargin=*}
\RequirePackage{csquotes}
\RequirePackage{scrlayer-scrpage}
\clearpairofpagestyles
\automark[section]{chapter}
\ihead{\headmark}
\ofoot*{\pagemark}
\setkomafont{pagehead}{\normalfont\small\sffamily\setstretch{1}\color{LawMuted}}
\setkomafont{pagefoot}{\normalfont\small\sffamily\setstretch{1}}
\setkomafont{disposition}{\normalfont\sffamily\bfseries\color{LawInk}}
\setkomafont{chapter}{\normalfont\LARGE\bfseries\color{LawInk}}
\RedeclareSectionCommand[beforeskip=18pt,afterskip=22pt]{chapter}
\setlength{\parindent}{1.2em}
\setlength{\parskip}{0.25ex plus 0.1ex}
\setlength{\emergencystretch}{1.5em}
\clubpenalty=8000
\widowpenalty=8000
\displaywidowpenalty=8000
\interfootnotelinepenalty=5000
\deffootnote[1.7em]{1.7em}{1em}{\textsuperscript{\thefootnotemark}}
\RequirePackage{hyperref}
\hypersetup{unicode=true,bookmarksnumbered=true,pdfdisplaydoctitle=true,pdflang={en-GB},colorlinks=true,linkcolor=LawInk,citecolor=LawInk,urlcolor=LawAccent}
\ifLawPrint\hypersetup{hidelinks}\fi
\RequirePackage{bookmark}
\RequirePackage{legalcite}
\ifLawReview
  \RequirePackage[pagewise]{lineno}
\fi
\newcommand{\LawPrompt}[1]{\par\smallskip\begingroup\small\color{LawMuted}\noindent\textbf{Author prompt.} #1\par\endgroup\smallskip}
\newcommand{\LawExampleNote}[1]{\par\smallskip\begingroup\small\color{LawMuted}\noindent\textbf{Working example.} #1\par\endgroup\smallskip}
\newcommand{\LawTODO}[1]{\textbf{[TODO: #1]}}
\newcommand{\LawChapterRef}[1]{Chapter~\ref{#1}}
\newcommand{\LawSectionRef}[1]{section~\ref{#1}}
\newcommand{\LawMetadata}{%
  \ifLawAnonymous
    \hypersetup{pdftitle={\ThesisTitle},pdfauthor={},pdfsubject={Anonymous review copy},pdfkeywords={}}%
  \else
    \hypersetup{pdftitle={\ThesisTitle},pdfauthor={\ThesisAuthor},pdfsubject={\ThesisSubtitle},pdfkeywords={\ThesisKeywords}}%
  \fi}
\newcommand{\MakeLawTitle}{%
  \ifLawAnonymous\LawGenericTitle\else
  \ifLawGroningen
    \IfFileExists{frontmatter/approved-title.pdf}{%
      \includepdf[pages=-,pagecommand={},width=\paperwidth,height=\paperheight,keepaspectratio]{frontmatter/approved-title.pdf}%
    }{\LawGenericTitle}%
  \else\LawGenericTitle\fi\fi}
\newcommand{\LawGenericTitle}{%
  \begin{titlepage}
    \thispagestyle{empty}
    \begingroup\setstretch{1.05}\setlength{\parindent}{0pt}
    \noindent{\sffamily\small\color{LawAccent}\ThesisDocumentLabel\par}
    \vspace{18mm}
    {\raggedright\hyphenpenalty=10000\exhyphenpenalty=10000\color{LawInk}\huge\bfseries\ThesisTitle\par}
    \vspace{6mm}
    {\Large\ThesisSubtitle\par}
    \vspace{12mm}
    {\color{LawAccent}\rule{22mm}{1.1pt}\par}
    \vspace{10mm}
    \ifLawAnonymous
      {\large Anonymous review copy\par}
    \else
      {\Large\ThesisAuthor\par}
      \vspace{5mm}
      {\ThesisFaculty\par\ThesisUniversity\par}
      \vspace{7mm}
      {\small\textbf{Supervision}\par\ThesisSupervisors\par}
    \fi
    \vfill
    {\small\ThesisDegree\par\ThesisDate\par}
    \vspace{4mm}
    {\small\color{LawMuted}Legal research cut-off: \ThesisLegalCutoff\par}
    \ifLawGroningen
      \vspace{3mm}{\small\bfseries Demonstration title page. Insert the approved institutional title page before submission.\par}
    \fi
    \endgroup
  \end{titlepage}}
\endinput
