import csv

# Open the input and output files
with open('cronlog2', 'r') as input_file, open('output.csv', 'w', newline='') as output_file:
    # Create the CSV writer object and write the header row
    csv_writer = csv.writer(output_file)
    csv_writer.writerow(['Time', 'Velocity_x', 'Velocity_y', 'Velocity_z', 'Velocity_Magnitude'])

    # Loop through each line in the input file
    for line_num, line in enumerate(input_file):
        # Check if the line is within the desired range
        if line_num >= 9 and line_num <= 33904:
            try:
              # Parse the time, velocity, and magnitude from the line
              line_parts = line.split()
              time = line_parts[1] + ' ' + line_parts[2]
              velocity_x = line_parts[4].replace('(', '')
              velocity_x = velocity_x.replace(',', '')
              velocity_y = line_parts[5].replace(',', '')
              velocity_z = line_parts[6].replace(')', '')
              velocity_magnitude = line_parts[8]

              # Write the parsed values to the output file as a new row
              csv_writer.writerow([time, velocity_x, velocity_y, velocity_z, velocity_magnitude])
            except Exception as e:
              print(f'Error parsing line {line_num}: {e} : {line}')
