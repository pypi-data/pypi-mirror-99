#!/bin/sh

startdir=$PWD

tmp=$(mktemp)
echo "Creating temporary environment in: $tmp"
echo ""

rm -rf $tmp
mkdir -p $tmp
cd $tmp

python3 -m venv venv
source venv/bin/activate

pip install darshan

echo ""
echo "PyDarshan version is:"
python -m darshan --version


echo ""
echo "Test a log can be succesfully parsed:"
python -m darshan info $startdir/../examples/example-logs/ior_hdf5_example.darshan



echo ""
read -p "Purge temporary directory $tmp ? [y/N]" -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
	rm -rf $tmp
fi
