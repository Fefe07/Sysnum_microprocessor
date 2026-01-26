include config.mk

% : %.py
	mkdir -p build
	$(PYTHON_INTERPRETER) $(CAROTTE_PATH) -o ./build/$@.net ./$@.py
	cp ./build/$@.net ./build/current.net 

sim : $(SIMULATOR)
	$(SIMULATOR) ./build/current.net

all :
	make alu log_unit arith_unit demux mux regs forwarding hazards

$(SIMULATOR_DIR)/netlist_simulator.byte :
	make -C $(SIMULATOR_DIR) build
	
cpu_pipeline: cpu_pipeline.py
	mkdir -p build
	$(PYTHON_INTERPRETER) $(CAROTTE_PATH) -o ./build/cpu_pipeline.net ./cpu_pipeline.py
	cp ./build/cpu_pipeline.net ./build/current.net

sim_pipeline : $(SIMULATOR)
	$(SIMULATOR) -n 30 ./build/current.net

clean :
	rm -rf ./build/
	rm -rf ./__pycache__/

.PHONY: sim clean
