# thesis_code

Where to find important code:

- The logic for the ensemble can be found in ensemble.py
- The file group.py contains a manual attempt to share fire locations and is used as inspiration for the ensemble information sharing
- The file plugin.py contains auxiliary functions
- The file sequence_rules.py contains the set of rules and behaviours used in the tests
- The file state_machine.py and state.py contains the logic of how tasks are shared inside the ensemble

ALGORITHM:

- simple test to try out -> python swarming.py - basic swarming algorithm
- spreading.py test the spreading algorithm
- spread_swarm.py tests how UAVs switch from one task to the other
- fire_fight_scenario.py tests a more complex scenario, involving multiple roles and tasks.

TESTS:

- file swarm_packet_loss_test.py shows the basic logic behind the reliability tests. This file tests the swarming algorithm executing every percentage of packets lost 10 times calculating average and std. The entire process is automatize and can be applied to all agorithm by changing the completion condition and the algorithm function call. 





