
#!/bin/sh

# All the output will be stored in a new directory. outdir. For every run outdir will be different.
unique_hash=$(openssl rand -hex 12 | md5)
outdir="ec-$unique_hash"

echo "Making output directory: $outdir"

dataoutdir="$outdir/Data"
plotsoutdir="$outdir/Plots"
pythonscript="main.py"
rscript="graphs.R"

# Check if the output directory for the python script exists
if [ ! -d "$dataoutdir" ]; then
    echo "Making directory $dataoutdir"
    mkdir -p "$dataoutdir"
fi

# Run the Python code.
echo "Running experiments..."
python "$pythonscript" "$dataoutdir"

# Now run the R script that generates the graphs
if [ ! -d "$plotsoutdir" ]; then
    echo "Making directory $plotsoutdir"
    mkdir -p "$plotsoutdir"
fi

echo "Generating plots..."
Rscript --vanilla "${rscript}" "${plotsoutdir}" "${dataoutdir}"

# Cleanup the .pyc files
rm -r *.pyc
echo "Done."