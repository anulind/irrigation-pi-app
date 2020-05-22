# Just a precaution...
screen -X -S irrigation_system quit

# Run test file
python3 "./test.py" $1
