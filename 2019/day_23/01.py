import intcode

#######################################################################
# SETUP 50 COMPUTERS
#######################################################################
NUMBER_COMPUTERS = 50
program_states = {}
packet_queue = []
invalid_packet_queue = []


print("Loading Computers")
for c in range(NUMBER_COMPUTERS):
    initial_state = intcode.load_file_into_memory('input23.txt')
    initial_state['haltFor'] = ['INPUT', 'OUTPUT']
    initial_state['inIo'].append(c)
    program_states[c] = initial_state
print("Computers Loaded")

#######################################################################
# MAIN EXECUTION LOOP
# Loops through each program state in turn if 3 values are output
# use them to construct a packet to add to the queue. After the 3rd
# packet move on. If a computer requests input then just provide a -1
# Next loop through the packet queue adding each to the input
# of the addressed computer (if it is valid)
#######################################################################
run = True

print("Computers Loaded")
while run:
    for c in range(NUMBER_COMPUTERS):
        received_packet = []

        while program_states[c]['haltState'] == 'RUNNING' and len(received_packet) < 3:
            program_states[c] = intcode.execute_interactive(program_states[c])

            if program_states[c]['haltState'] == 'HALTED_OUTPUT':
                print('HALT')
                break

            if program_states[c]['haltState'] == 'PAUSE_OUTPUT':
                program_states[c]['haltState'] = 'RUNNING'
                if len(program_states[c]['outIo']) == 1:
                    received_packet.append(program_states[c]['outIo'][0])
                    program_states[c]['outIo'] = []

            if program_states[c]['haltState'] == 'PAUSE_INPUT':
                program_states[c]['haltState'] = 'RUNNING'
                program_states[c]['inIo'].append(-1)
                break

        if len(received_packet) > 0:
            packet_queue.append(received_packet)

        while len(packet_queue) > 0:
            packet = packet_queue.pop(0)
            address = packet[0]

            # Filter out invalid packets
            if address < 0 or address > NUMBER_COMPUTERS:
                invalid_packet_queue.append(packet)
                if address == 255:
                    print("packet to 255: ", packet)
                    run = False
            else:
                packet_x, packet_y = packet[1], packet[2]
                program_states[address]['inIo'].append(packet_x)
                program_states[address]['inIo'].append(packet_y)

print(packet_queue)
print(invalid_packet_queue)
