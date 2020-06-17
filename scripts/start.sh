# Make sure program is not already running
screen -X -S irrigation_system quit

# Start program
screen -S irrigation_system python3 -u ./main.py
