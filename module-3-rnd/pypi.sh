while read line; do
    sudo /home/shreyas/Downloads/fall-2022/capstone/code/package-analysis/run_analysis.sh pypi "$line"
done < top-10-pypi.txt
