#!/usr/bin/env zsh


CLONE_DIR='/path/to/emrakuls/qiime2'
CONDA_ENV='emrakul'
QIIME_REPOS=('qiime2' 'q2cli' 'q2templates' 'q2-types' 'q2-feature-table'
             'q2-diversity' 'q2-emperor' 'q2-demux' 'q2-alignment'
             'q2-phylogeny' 'q2-dada2' 'q2-composition' 'q2-taxa'
             'q2-feature-classifier')

local -a unstaged=()
cd $CLONE_DIR
source activate $CONDA_ENV
for repo in $QIIME_REPOS; do
    cd $repo
    if ! git diff-index --quiet HEAD --
    then
        unstaged+=($repo)
    else
        git checkout master &&
        git pull upstream master &&
        git push origin master
    fi

    yes | pip uninstall $repo
    pip install -e .

    cd ..
done

for repo in $unstaged; do
    echo -e "\e[0;31m Unstaged changes in: $unstaged"
done
